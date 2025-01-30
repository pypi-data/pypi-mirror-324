from enum import Enum
import logging
import os

from fastapi import HTTPException, Request
from gandalf import AuthorizationClient
import gandalf.authz_request_pb2 as authz_request_pb2
import nflxenv
from nflx_security_util import AuthorizableContext, get_authorized_caller
from nflx_security_util.utils import NflxSecurityUtilException
from spectator import GlobalRegistry

from api_gateway.models.tool_models import Permissions

logger = logging.getLogger(__name__)


class PermissionLevel(Enum):
    BASIC: str = "basic"
    OWNER: str = "owner"


AUTH_SOURCE_API = "api"
AUTH_SOURCE_TOOL = "tool"


# Stolen from: https://github.netflix.net/corp/ncp-copilot-dp-python/blob/main/copilot_dp_python/gandalf_helper.py
def _is_running_under_test():
    return "PYTEST_CURRENT_TEST" in os.environ


def get_gandalf_client():
    if nflxenv.is_local_dev() or _is_running_under_test():
        import gandalfagent

        agent = gandalfagent.AgentProcessManager()
        return AuthorizationClient(socket_path=agent.getSocketPath())

    return AuthorizationClient()


gandalf_client = get_gandalf_client()


def construct_authorizable_context(caller_context: AuthorizableContext):
    gandalf_context = authz_request_pb2.AuthorizableContext(
        enforcement_mode=authz_request_pb2.AuthorizableContext.EnforcementMode.ENFORCE_ALL
    )

    # There has to be a better way to do this
    if caller_context.initial.identityType == "User":
        # caller_name = caller_context.initial.identity.username
        gandalf_context.initial.user_authorizable_identity.username = caller_context.initial.identity.username
        gandalf_context.initial.user_authorizable_identity.user_id = caller_context.initial.identity.userId
        gandalf_context.initial.user_authorizable_identity.domain = caller_context.initial.identity.domain
    elif caller_context.initial.identityType == "Application":
        # caller_name = caller_context.initial.identity.applicationName
        gandalf_context.initial.application_authorizable_identity.application_name = caller_context.initial.identity.applicationName
        gandalf_context.initial.application_authorizable_identity.account_id = caller_context.initial.identity.accountId

    # From what I've seen there always needs to be an intial caller, so no need to fallback on direct (is this true?)
    # else:
    #     if caller_context.direct.identityType == "User":
    #         caller_name = caller_context.direct.identity.username
    #         gandalf_context.direct.user_authorizable_identity.username = caller_context.direct.identity.username
    #         gandalf_context.direct.user_authorizable_identity.user_id = caller_context.direct.identity.userId
    #         gandalf_context.direct.user_authorizable_identity.domain = caller_context.direct.identity.domain
    #     elif caller_context.direct.identityType == "Application":
    #         caller_name = caller_context.direct.identity.applicationName
    #         gandalf_context.direct.application_authorizable_identity.application_name = caller_context.direct.identity.applicationName
    #         gandalf_context.direct.application_authorizable_identity.account_id = caller_context.direct.identity.accountId

    # Note the below doesn't seem to work (sending the auth context string then parsing makes auth check always fail)
    # # Stolen from https://github.netflix.net/corp/ncp-copilot-dp-python/blob/main/copilot_dp_python/gandalf_helper.py#L41
    # gandalf_context = authz_request_pb2.AuthorizableContext()
    # json_format.Parse(x_authorizable_ctx_json, gandalf_context)

    return gandalf_context


def _get_caller_context_and_log(request: Request, auth_source: str) -> AuthorizableContext:
    try:
        caller_context = get_authorized_caller(request)
        logger.debug("Authorized caller: %s", caller_context)

        if caller_context.initial.identityType == "User":
            GlobalRegistry.counter(
                "apigateway.initialCallerDetails",
                tags={"type": "user", "name": caller_context.initial.identity.username, "source": auth_source},
            ).increment()
            request.state.caller = {"username": caller_context.initial.identity.username, "app_name": None, "auth_source": auth_source}
        else:
            GlobalRegistry.counter(
                "apigateway.initialCallerDetails",
                tags={"type": "app", "name": caller_context.initial.identity.applicationName, "source": auth_source},
            ).increment()
            request.state.caller = {
                "username": None,
                "app_name": caller_context.initial.identity.applicationName,
                "auth_source": auth_source,
            }
        if caller_context.direct.identityType == "Application":
            request.state.caller["app_name"] = caller_context.direct.identity.applicationName
            GlobalRegistry.counter(
                "apigateway.directCallerApplication", tags={"app_name": caller_context.direct.identity.applicationName}
            ).increment()
        return caller_context
    except NflxSecurityUtilException as e:
        logger.error("Could not get authorized caller: %s", str(e))
        request.state.caller = {
            "username": "unknown",
            "app_name": None,
            "auth_source": auth_source,
        }

        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error("Could not get authorized caller: %s", str(e))
        request.state.caller = {
            "username": "unknown",
            "app_name": None,
            "auth_source": auth_source,
        }
        raise HTTPException(status_code=500, detail=str(e))


def is_authorized(
    request: Request, tool_permissions: Permissions, required_permission: PermissionLevel, auth_source: str = AUTH_SOURCE_API
) -> bool:
    # For some reason this is the only way to check if the header is missing because of local?
    headers = {k.lower(): v for k, v in request.headers.items()}
    x_authorizable_ctx_json = headers.get("x-authorizable-ctx-json")

    if not x_authorizable_ctx_json:
        if nflxenv.is_local_dev():
            GlobalRegistry.counter("apigateway.callerDetails", tags={"username": "local", "source": auth_source}).increment()
            request.state.caller = {"username": "local", "app_name": None, "auth_source": auth_source}
            return True
        logger.warning("Unauthorized caller: Authorizable context not in header.")
        return False

    try:
        caller_context = _get_caller_context_and_log(request, auth_source)
    except HTTPException as e:
        logger.warning("Could not get authorized caller: %s", str(e))
        return False

    if tool_permissions.accessibility == "public" and required_permission == PermissionLevel.BASIC:
        return True

    try:
        gandalf_context = construct_authorizable_context(caller_context)
        allowed_policies = [tool_permissions.owner.gandalf_policy]
        if required_permission == PermissionLevel.BASIC:
            allowed_policies += [project.gandalf_policy for project in tool_permissions.allowed_projects]

        logger.info("Checking all allowed policies: %s", allowed_policies)
        for policy in allowed_policies:
            res = gandalf_client.isAuthorizedByPolicyNameByAuthorizableContext(
                policy,
                gandalf_context,
                custom_context=None,
            )
            if res.allowed:
                logger.info(
                    "Authorization check (level %s) passed for caller %s and policy %s", required_permission, gandalf_context, policy
                )
                return True

        logger.info("Authorization check (level %s)failed for caller %s", required_permission, gandalf_context)
        return False

    except Exception as e:
        logger.error("Exception during authorization check: %s", str(e))
        return False
