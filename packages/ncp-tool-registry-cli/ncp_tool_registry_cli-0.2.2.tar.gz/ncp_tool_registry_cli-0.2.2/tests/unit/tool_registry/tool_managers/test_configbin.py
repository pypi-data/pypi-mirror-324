from src.api_gateway.models.tool_models import ConfigBinTool, Info, Permissions, GenAIProject
from src.api_gateway.tool_registry.tool_managers.configbin import get_tool_invocation_path


def test_get_tool_invocation_path():
    tool = ConfigBinTool(
        tool_id="test-tool",
        permissions=Permissions(
            owner=GenAIProject(env="test", project_id="test", gandalf_policy="test"),
            accessibility="public",
            allowed_projects=[],
        ),
        response_schema={},
        openapi="3.0.1",
        info=Info(title="Test Tool", description="A test tool", version="1.0.0"),
        request_schema={"get": {"operationId": "testOperation", "parameters": []}},
        invocation={"endpoint": "/api/v1/test/{param1}/{param2}", "method": "GET", "type": "metatron_endpoint"},
        components={"schemas": {}},
    )

    result = get_tool_invocation_path(tool)
    expected = "/ncp_model_gateway/v1/function/test-tool/invoke/{param1}/{param2}"
    assert result == expected
