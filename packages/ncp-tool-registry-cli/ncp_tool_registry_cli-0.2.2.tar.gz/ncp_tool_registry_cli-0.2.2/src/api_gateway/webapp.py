import logging
from typing import Any, Dict
from datetime import datetime
import time

import aiohttp
from nflxconfig import NXCONF
import nflxlog
import nflxtrace
from nflxlog.nflxlogger import NflxLogger
import nflxenv
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Body, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from nflx_security_util import get_authorized_caller
from nflx_security_util.utils import NflxSecurityUtilException
from contextlib import asynccontextmanager
from spectator import GlobalRegistry
from nflxmetrics.fastapi_middleware import MetricsMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from api_gateway.logging.metrics_client import MetricsClient
from api_gateway.logging.models import ToolInvocationMetric
from api_gateway.services.gandalf_helper import is_authorized, PermissionLevel, AUTH_SOURCE_TOOL
from api_gateway.services.gateway_service import process_schema, log_latencies_to_atlas
from api_gateway.services.tool_invoker import ToolInvoker
from api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager
from api_gateway.tool_registry.tool_managers.danswer import DanswerToolManager
from api_gateway.tool_registry.tool_registry_controller import router as tool_registry_router
from api_gateway.dependencies import get_configbin_manager, get_metrics_client, get_tool_invoker
from api_gateway.tool_registry.tool_registry_operations import ToolRegistryOperations


NXCONF.defaults.load_config(__file__)
logger = NflxLogger(__name__)
logger.configure()
nflxlog.init()
logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
nflxtrace.trace_init()
nflxtrace.instrument_auto()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.configbin_manager = ConfigbinManager(env=nflxenv.nf_env("test"))
        app.state.configbin_manager.sync_tool_registry()
        logger.info("Successfully loaded tools from ConfigBin")

        app.state.danswer_manager = DanswerToolManager(env=nflxenv.nf_env("test"))
        logger.info("Successfully set up Danswer manager")

        app.state.tool_registry_ops = ToolRegistryOperations(app.state.configbin_manager, app.state.danswer_manager)
        app.state.tool_invocation_metrics_client = MetricsClient[ToolInvocationMetric]("api_gateway_test")

        app.state.tool_invoker = ToolInvoker()
        await app.state.tool_invoker.initialize()
        logger.info("Successfully initialized tool invoker")

    except Exception as e:
        logger.error("Failed to initialize services: %s", e)
        raise

    yield

    logger.info("Shutting down application...")
    try:
        await app.state.tool_invocation_metrics_client.cleanup()
        logger.info("Successfully cleaned up tool metrics client")

        await app.state.tool_invoker.cleanup()
        logger.info("Successfully cleaned up tool invoker")
    except Exception as e:
        logger.error("Error during cleanup: %s", e)

    app.state.configbin_manager = None
    app.state.danswer_manager = None
    app.state.tool_registry_ops = None
    app.state.tool_invocation_metrics_client = None
    app.state.tool_invoker = None


APP = FastAPI(lifespan=lifespan)

APP.add_middleware(SentryAsgiMiddleware)
APP.add_middleware(MetricsMiddleware)

APP.include_router(tool_registry_router)

nflxtrace.instrument_fastapi_app(APP)


@APP.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


@APP.api_route(
    "/ncp_model_gateway/v1/function/{tool_id}/invoke",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    operation_id="gateway_invoke",
    tags=["API Gateway"],
)
@APP.api_route(
    "/ncp_model_gateway/v1/function/{tool_id}/invoke/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    operation_id="gateway_invoke_with_path",
    tags=["API Gateway"],
)
async def gateway(
    tool_id: str,
    request: Request,
    body: Dict[str, Any] = Body(default=None),
    path: str = None,
    configbin_manager: ConfigbinManager = Depends(get_configbin_manager),
    tool_invocation_metrics_client: MetricsClient = Depends(get_metrics_client),
    tool_invoker: ToolInvoker = Depends(get_tool_invoker),
):
    request.state.start_time = time.time()
    configbin_manager.sync_tool_registry()
    tool = configbin_manager.get_tool_by_id(tool_id)
    if not tool:
        configbin_manager.sync_tool_registry()
        tool = configbin_manager.get_tool_by_id(tool_id)
        if not tool:
            tool_not_found_message = f"ERROR! Tool not found: {tool_id}"
            logger.error(tool_not_found_message)
            raise HTTPException(status_code=404, detail=tool_not_found_message)

    logger.info(f"Checking authorization for tool {tool_id}")
    authorized = is_authorized(request, tool.permissions, PermissionLevel.BASIC, AUTH_SOURCE_TOOL)
    caller = request.state.caller
    if not authorized:
        unauthorized_message = f"ERROR! Unauthorized to call tool: {tool_id}"
        logger.error(unauthorized_message)
        tool_invocation_metrics_client.log_metric(
            ToolInvocationMetric(
                timestamp=datetime.now().isoformat(),
                tool_id=tool_id,
                username=caller.get("username"),
                app_name=caller.get("app_name"),
                project_id=tool.permissions.owner.project_id,
                accessibility=tool.permissions.accessibility,
                auth_source=AUTH_SOURCE_TOOL,
                success=False,
                error=unauthorized_message,
            )
        )
        raise HTTPException(status_code=403, detail=unauthorized_message)

    logger.info(f"Calling tool: {tool_id}")
    GlobalRegistry.counter("apigateway.invokedToolOwnerProject", tags={"project_id": tool.permissions.owner.project_id}).increment()

    try:
        response = await tool_invoker.invoke_tool(tool, request, additional_path=path)
        GlobalRegistry.counter(
            "apigateway.invokedTool", tags={"tool_id": tool_id, "accessibility": tool.permissions.accessibility, "error": "None"}
        ).increment()
        tool_invocation_metrics_client.log_metric(
            ToolInvocationMetric(
                timestamp=datetime.now().isoformat(),
                tool_id=tool_id,
                username=caller.get("username"),
                app_name=caller.get("app_name"),
                project_id=tool.permissions.owner.project_id,
                accessibility=tool.permissions.accessibility,
                auth_source=AUTH_SOURCE_TOOL,
                success=True,
                error=None,
            )
        )

        if response is None:
            logger.info("Response: None received from tool")
            log_latencies_to_atlas(request=request, tool_id=tool_id)

            # We still want to let the LLM know the tool was successfully called even if there is no response
            return f"Success! Done calling tool: {tool_id}"

        if tool.postprocessing_jsonpath:
            try:
                if not isinstance(response, (dict, list)):
                    logger.warning("Skipping postprocessing: response is not JSON (not dict or list)")
                else:
                    filtered = process_schema(response, tool.postprocessing_jsonpath)
                    logger.info("Applied postprocessing: original length %s, filtered length %s", len(str(response)), len(str(filtered)))
                    if filtered is not None:
                        logger.info("Final response: %s", str(filtered)[:500])
                        log_latencies_to_atlas(request=request, tool_id=tool_id, postprocessing="true")
                        return filtered
            except Exception as e:
                logger.warning("Failed to apply postprocessing: %s", e)

        logger.info("Final response: %s", str(response)[:500])
        log_latencies_to_atlas(request=request, tool_id=tool_id)
        return response

    except aiohttp.ClientResponseError as http_error:
        GlobalRegistry.counter(
            "apigateway.invokedTool",
            tags={"tool_id": tool_id, "accessibility": tool.permissions.accessibility, "error": http_error.strerror},
        ).increment()
        tool_invocation_metrics_client.log_metric(
            ToolInvocationMetric(
                timestamp=datetime.now().isoformat(),
                tool_id=tool_id,
                username=caller.get("username"),
                app_name=caller.get("app_name"),
                project_id=tool.permissions.owner.project_id,
                accessibility=tool.permissions.accessibility,
                auth_source=AUTH_SOURCE_TOOL,
                success=False,
                error=http_error.strerror,
            )
        )
        log_latencies_to_atlas(request=request, tool_id=tool_id, error=http_error.strerror)
        error_message = f"ERROR! Failed to call tool with HTTPException: {http_error}"
        logger.error(error_message)
        raise HTTPException(status_code=http_error.status, detail=error_message)
    except Exception as e:
        GlobalRegistry.counter(
            "apigateway.invokedTool", tags={"tool_id": tool_id, "accessibility": tool.permissions.accessibility, "error": str(e)}
        ).increment()
        tool_invocation_metrics_client.log_metric(
            ToolInvocationMetric(
                timestamp=datetime.now().isoformat(),
                tool_id=tool_id,
                username=caller.get("username"),
                app_name=caller.get("app_name"),
                project_id=tool.permissions.owner.project_id,
                accessibility=tool.permissions.accessibility,
                auth_source=AUTH_SOURCE_TOOL,
                success=False,
                error=str(e),
            )
        )
        log_latencies_to_atlas(request=request, tool_id=tool_id, error=str(e))
        error_message = f"ERROR! Failed to call tool with exception: {e}"
        logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)


@APP.get("/protected", tags=["API Gateway"])
async def protected(request: Request) -> str:
    """
    Example on how to use nflx-security-util
    for authZ.
    """
    try:
        caller = get_authorized_caller(request)  # extract information about direct/initial caller identity
    except NflxSecurityUtilException as e:
        raise HTTPException(status_code=403, detail=str(e))

    # example for matching direct caller identity type
    if caller.direct.identityType == "User":
        return f"Email: {caller.direct.identity.username}"
        # even more details about a User can be extracted with caller.direct.identity.get_user_details()
    elif caller.direct.identityType == "Application":
        return f"Application Name: {caller.direct.identity.applicationName}"
    else:
        return f"Identity: {caller.direct.identityType}"


@APP.get("/healthcheck", tags=["API Gateway"])
async def healthcheck() -> str:
    GlobalRegistry.counter("apigateway.healthcheck").increment()
    return "OK"


if __name__ == "__main__":
    port = NXCONF.get_int("server.port", 7101)
    logger.info(f"Starting server on port {port}")
    uvicorn.run("api_gateway.webapp:APP", host="0.0.0.0", port=port, log_level="info", reload=True)
