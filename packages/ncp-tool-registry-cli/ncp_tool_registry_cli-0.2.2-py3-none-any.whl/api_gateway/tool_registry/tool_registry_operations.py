import json
import logging
from typing import Dict, Optional
import requests


from api_gateway.services.gateway_service import process_schema
from api_gateway.models.tool_models import (
    ConfigBinTool,
    CreateToolRequest,
    ConfigBinToolConfig,
    Info,
    RegistryTool,
    GenAIProject,
    Permissions,
    UpdateToolRequest,
    ReconfigureToolRequest,
)
from api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager
from api_gateway.tool_registry.tool_managers.danswer import DanswerToolManager
from api_gateway.tool_registry.utils.discovery import discover_openapi, get_app_name, get_endpoint_schemas_and_components
from api_gateway.tool_registry.utils.ncp_project_connection import get_gandalf_policy_from_ncp_project
from api_gateway.tool_registry.utils.validators import is_valid_id, is_valid_jsonpath

logger = logging.getLogger(__name__)


class ToolRegistryOperations:
    def __init__(self, configbin_manager: ConfigbinManager, danswer_manager: DanswerToolManager):
        self.configbin_manager = configbin_manager
        self.danswer_manager = danswer_manager

    def list_tools(self) -> Dict[str, ConfigBinToolConfig]:
        return self.configbin_manager.list_tools()

    def register_tool(
        self, tool_id: str, tool_request: CreateToolRequest, sync_to_danswer: bool = True, reconfiguring_tool: bool = False
    ) -> RegistryTool:
        logger.info(f"Registering tool {tool_id}")
        self.sync_registry()

        if not is_valid_id(tool_id):
            raise ValueError("Invalid tool_id! Please use only alphanumeric characters, underscores, and dashes.")

        if self.get_tool(tool_id=tool_id, ignore_error=True) and not reconfiguring_tool:
            raise ValueError(f"Tool id {tool_id} already exists! Please choose a different tool id.")

        owner_gandalf_policy = get_gandalf_policy_from_ncp_project(tool_request.owner.project_id, tool_request.owner.env)
        if not owner_gandalf_policy:
            raise ValueError("Could not fetch Gandalf policy for given owner NCP project id and env.")

        owner_project = GenAIProject(
            env=tool_request.owner.env,
            project_id=tool_request.owner.project_id,
            gandalf_policy=owner_gandalf_policy,
        )

        allowed_projects = []
        for project in tool_request.allowed_projects:
            project_gandalf_policy = get_gandalf_policy_from_ncp_project(project.project_id, project.env)
            if not project_gandalf_policy:
                raise ValueError(
                    f"Could not fetch Gandalf policy for given project in allowed_projects: {project.project_id} ({project.env})."
                )
            allowed_projects.append(GenAIProject(env=project.env, project_id=project.project_id, gandalf_policy=project_gandalf_policy))

        permissions = Permissions(
            owner=owner_project,
            accessibility=tool_request.accessibility,
            allowed_projects=allowed_projects,
        )

        spec = discover_openapi(tool_request.base_url)
        if not spec:
            raise ValueError("Could not find OpenAPI docs for provided URL.")

        request_schemas, components, response_schemas = get_endpoint_schemas_and_components(
            path=tool_request.path, methods=tool_request.methods, spec=spec
        )
        for method in tool_request.methods:
            if method not in request_schemas:
                raise ValueError(f"Method {method} not found in OpenAPI spec for path {tool_request.path}")

        if tool_request.preprocessing_jsonpath:
            if (
                not is_valid_jsonpath(tool_request.preprocessing_jsonpath)
                or type(process_schema(request_schemas, tool_request.preprocessing_jsonpath)) is not dict
            ):
                raise ValueError("Invalid preprocessing_jsonpath")
            else:
                # Currently doing this here so LLM generates request with preprocessing applied (instead of generating full request and then preprocessing)
                request_schemas = process_schema(request_schemas, tool_request.preprocessing_jsonpath)

        if tool_request.postprocessing_jsonpath and not is_valid_jsonpath(tool_request.postprocessing_jsonpath):
            raise ValueError("Invalid postprocessing_jsonpath")

        invocation = {"endpoint": tool_request.base_url + tool_request.path}
        if "netflix" in tool_request.base_url:
            invocation["type"] = "metatron_endpoint"
            invocation["app_name"] = get_app_name(tool_request.base_url)

        tool = RegistryTool(
            tool_id=tool_id,
            info=Info(title=tool_request.info.title, description=tool_request.info.description, version=tool_request.info.version),
            openapi=spec["openapi"],
            permissions=permissions,
            invocation=invocation,
            request_schema=request_schemas,
            preprocessing_jsonpath=tool_request.preprocessing_jsonpath,
            response_schema=response_schemas,
            postprocessing_jsonpath=tool_request.postprocessing_jsonpath,
            components=components,
        )

        if reconfiguring_tool:
            return self.update_tool(tool_id, UpdateToolRequest(**tool.model_dump()))
        else:
            return self.add_tool(tool, sync_to_danswer=sync_to_danswer)

    def add_tool(self, tool: RegistryTool, sync_to_danswer: bool = True) -> RegistryTool:
        logger.info(f"Adding tool {tool.tool_id}")
        configbin_tool = ConfigBinTool(**tool.model_dump())
        self.configbin_manager.add_tool_to_configbin(configbin_tool, f"Create tool {tool.tool_id}")
        if sync_to_danswer:
            self.danswer_manager.add_single_tool(configbin_tool)
        return tool

    def get_tool(self, tool_id: str, ignore_error: bool = False) -> RegistryTool:
        configbin_tool = self.configbin_manager.get_tool_by_id(tool_id, ignore_error=ignore_error)
        if not configbin_tool:
            return None
        return RegistryTool(**configbin_tool.model_dump())

    def delete_tool(self, tool_id: str) -> str:
        logger.info(f"Deleting tool {tool_id}")
        tool = self.configbin_manager.get_tool_by_id(tool_id)
        if not tool:
            raise ValueError(f"Tool not found: {tool_id}")

        self.configbin_manager.delete_tool(tool_id, f"Delete tool {tool_id}")
        self.danswer_manager.delete_tool(tool.info.title)
        return f"Tool {tool_id} successfully deleted."

    def update_tool(self, tool_id: str, update_tool_request: UpdateToolRequest) -> RegistryTool:
        logger.info(f"Updating tool {tool_id}")
        tool = self.configbin_manager.get_tool_by_id(tool_id, ignore_error=True)
        if not tool:
            raise ValueError(f"Tool not found: {tool_id}")

        if not is_valid_jsonpath(update_tool_request.preprocessing_jsonpath):
            raise ValueError("Invalid preprocessing_jsonpath")

        if not is_valid_jsonpath(update_tool_request.postprocessing_jsonpath):
            raise ValueError("Invalid postprocessing_jsonpath")

        # TODO: Add validation for other fields since the user is passing them directly

        old_title = tool.info.title
        updated_tool = tool.model_dump()
        if update_tool_request.info:
            if update_tool_request.info.title:
                updated_tool["info"]["title"] = update_tool_request.info.title
            if update_tool_request.info.description:
                updated_tool["info"]["description"] = update_tool_request.info.description
            if update_tool_request.info.version:
                updated_tool["info"]["version"] = update_tool_request.info.version
        if update_tool_request.openapi:
            updated_tool["openapi"] = update_tool_request.openapi
        if update_tool_request.permissions:
            if update_tool_request.permissions.owner:
                updated_tool["permissions"]["owner"] = update_tool_request.permissions.owner.model_dump()
            if update_tool_request.permissions.accessibility:
                updated_tool["permissions"]["accessibility"] = update_tool_request.permissions.accessibility
            if update_tool_request.permissions.allowed_projects:
                updated_tool["permissions"]["allowed_projects"] = [
                    project.model_dump() for project in update_tool_request.permissions.allowed_projects
                ]
        if update_tool_request.invocation:
            updated_tool["invocation"] = update_tool_request.invocation
        if update_tool_request.request_schema:
            updated_tool["request_schema"] = update_tool_request.request_schema
        if update_tool_request.preprocessing_jsonpath:
            updated_tool["preprocessing_jsonpath"] = update_tool_request.preprocessing_jsonpath
        if update_tool_request.response_schema:
            updated_tool["response_schema"] = update_tool_request.response_schema
        if update_tool_request.postprocessing_jsonpath:
            updated_tool["postprocessing_jsonpath"] = update_tool_request.postprocessing_jsonpath
        if update_tool_request.components:
            updated_tool["components"] = update_tool_request.components

        self.configbin_manager.update_tool(updated_tool=ConfigBinTool.model_validate(updated_tool))
        self.danswer_manager.update_tool(old_title=old_title, updated_tool=ConfigBinTool.model_validate(updated_tool))
        return RegistryTool(**updated_tool)

    def reconfigure_tool(self, tool_id: str, reconfigure_tool_request: ReconfigureToolRequest) -> RegistryTool:
        logger.info("Reconfiguring tool %s", tool_id)
        tool = self.configbin_manager.get_tool_by_id(tool_id, ignore_error=True)
        if not tool:
            logger.error("Tool %s not found", tool_id)
            raise ValueError(f"Tool not found: {tool_id}. Please register the tool first.")

        return self.register_tool(tool_id=tool_id, tool_request=reconfigure_tool_request, reconfiguring_tool=True)

    def sync_tool_to_danswer(self, tool_id: str) -> str:
        logger.info(f"Syncing tool {tool_id} to Danswer")
        tool = self.configbin_manager.get_tool_by_id(tool_id)
        if not tool:
            self.configbin_manager.sync_tool_registry()
            tool = self.configbin_manager.get_tool_by_id(tool_id)
            if not tool:
                raise ValueError(f"Tool not found: {tool_id}")

        if self.danswer_manager.add_single_tool(tool):
            return f"Tool {tool_id} successfully synced to Danswer."
        return f"Tool {tool_id} already present in Danswer."

    def sync_registry(self) -> None:
        self.configbin_manager.sync_tool_registry()

    def fetch_graphql_schema(self, base_url: str) -> Optional[dict]:
        introspection_query = """
        query IntrospectionQuery {
          __schema {
            types {
              name
              fields {
                name
                type {
                  name
                  kind
                  ofType {
                    name
                    kind
                  }
                }
              }
            }
          }
        }
        """

        headers = {
            "Content-Type": "application/json",
        }

        payload = {"query": introspection_query}

        try:
            response = requests.post(base_url, json=payload, headers=headers)
            response.raise_for_status()
            schema = response.json()
            logger.debug(f"GraphQL Schema: {json.dumps(schema, indent=2)}")
            return schema
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching GraphQL schema: {e}")
            return None
