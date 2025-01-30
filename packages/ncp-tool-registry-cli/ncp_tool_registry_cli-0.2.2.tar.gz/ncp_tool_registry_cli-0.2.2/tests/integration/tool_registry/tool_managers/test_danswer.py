import pytest
from src.api_gateway.tool_registry.tool_managers.danswer import DanswerToolManager
from src.api_gateway.models.tool_models import ConfigBinTool, Info, Permissions, GenAIProject


@pytest.fixture(autouse=True)
def cleanup():
    yield
    manager = DanswerToolManager(env="test")
    tool_title = "Integration Test Tool"
    if manager.is_tool_present(tool_title):
        manager.delete_tool(tool_title)


def test_danswer_manager_tool_lifecycle():
    configbin_tool = ConfigBinTool(
        tool_id="integration-test-tool",
        permissions=Permissions(
            owner=GenAIProject(env="test", project_id="test", gandalf_policy="test"),
            accessibility="public",
            allowed_projects=[],
        ),
        response_schema={"post": {"200": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/Query"}}}}}},
        openapi="3.1.0",
        request_schema={
            "post": {
                "operationId": "test_operation",
                "summary": "Test operation",
                "parameters": [{"in": "query", "name": "query", "required": True, "schema": {"$ref": "#/components/schemas/Query"}}],
            }
        },
        invocation={"endpoint": "https://test-api.example.com/v1/test", "type": "test_endpoint"},
        info=Info(title="Integration Test Tool", description="Test tool description", version="1.0.0"),
        components={
            "schemas": {
                "Query": {
                    "type": "object",
                    "properties": {
                        "queryStr": {
                            "type": "string",
                        }
                    },
                }
            }
        },
    )

    manager = DanswerToolManager(env="test")
    tool_title = configbin_tool.info.title

    if manager.is_tool_present(tool_title):
        manager.delete_tool(tool_title)

    assert not manager.is_tool_present(tool_title)

    assert manager.add_single_tool(configbin_tool)

    assert manager.is_tool_present(tool_title)

    manager.delete_tool(tool_title)

    assert not manager.is_tool_present(tool_title)
