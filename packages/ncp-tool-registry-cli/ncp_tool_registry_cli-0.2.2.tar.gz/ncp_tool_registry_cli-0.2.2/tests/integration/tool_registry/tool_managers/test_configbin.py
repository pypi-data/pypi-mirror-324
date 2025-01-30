from typing import Optional
import pytest

from src.api_gateway.models.tool_models import ConfigBinTool, Info, Permissions, GenAIProject
from src.api_gateway.tool_registry.tool_managers.configbin import ConfigbinManager

from busypie import SECOND, wait_at_most


def poll_for_tool(
    configbin_manager, tool_id: str, wait_for_deletion: bool = False, timeout: float = 60.0, interval: float = 1.0
) -> Optional[ConfigBinTool]:
    def check_tool():
        tool = configbin_manager.get_tool_by_id(tool_id)

        # If we are waiting for deletion, we want to keep polling until the tool is deleted (tool is None).
        # Otherwise, we return tool and keep polling until it's present in ConfigBin (tool isn't None).
        return tool is None if wait_for_deletion else tool

    return wait_at_most(timeout, SECOND).return_on_timeout().poll_interval(interval, SECOND).until(check_tool)


@pytest.fixture
def configbin_manager():
    return ConfigbinManager(configbin_prefix="fassumpcao/test", env="test")


@pytest.fixture
def test_tool():
    return ConfigBinTool(
        tool_id="test_tool",
        permissions=Permissions(
            owner=GenAIProject(env="test", project_id="test", gandalf_policy="test"),
            accessibility="public",
            allowed_projects=[],
        ),
        response_schema={"type": "object"},
        openapi="3.0.0",
        info=Info(title="Test Tool", description="Test description", version="0"),
        request_schema={"post": {"type": "object"}},
        invocation={
            "endpoint": "http://api.example.com/api/v1/test/{param}",
        },
    )


@pytest.fixture(autouse=True)
def cleanup(configbin_manager, test_tool):
    yield
    if configbin_manager.get_tool_by_id(test_tool.tool_id):
        configbin_manager.delete_tool(test_tool.tool_id)
        configbin_manager.sync_tool_registry()


def test_configbin_manager_tool_lifecyle(configbin_manager, test_tool):
    existing_tool = configbin_manager.get_tool_by_id(test_tool.tool_id)
    if existing_tool:
        configbin_manager.delete_tool(test_tool.tool_id)
        configbin_manager.sync_tool_registry()
        assert poll_for_tool(configbin_manager, test_tool.tool_id, wait_for_deletion=True)

    configbin_manager.add_tool_to_configbin(test_tool)
    configbin_manager.sync_tool_registry()

    tool = poll_for_tool(configbin_manager, test_tool.tool_id)
    assert tool is not None
    assert tool.tool_id == "test_tool"

    all_tools = configbin_manager.list_tools()
    assert test_tool.tool_id in all_tools

    configbin_manager.delete_tool(test_tool.tool_id)
    configbin_manager.sync_tool_registry()

    assert poll_for_tool(configbin_manager, test_tool.tool_id, wait_for_deletion=True)


def test_tool_not_found(configbin_manager):
    non_existent_tool = configbin_manager.get_tool_by_id("non-existent-tool-id")
    assert non_existent_tool is None
