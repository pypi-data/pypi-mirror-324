from src.api_gateway.models.tool_models import ConfigBinTool, Info, Permissions, GenAIProject
from src.api_gateway.tool_registry.tool_managers.danswer import DanswerToolManager


def test_translate_configbin_tool_to_danswer_with_refs():
    configbin_tool = ConfigBinTool(
        tool_id="test-tool",
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
                "parameters": [{"in": "query", "name": "query", "required": True, "schema": {"$ref": "#/components/schemas/Query"}}],
            }
        },
        invocation={"endpoint": "https://test-api.example.com/v1/test", "type": "test_endpoint"},
        info=Info(title="Test Tool", description="Test tool description", version="1.0.0"),
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

    danswer_tool = DanswerToolManager.translate_configbin_tool_to_danswer(configbin_tool, "test")

    expected_tool_path = "/ncp_model_gateway/v1/function/test-tool/invoke"
    assert expected_tool_path in danswer_tool.definition.paths
    assert "post" in danswer_tool.definition.paths[expected_tool_path]

    # Check schema was dereferenced
    schema = danswer_tool.definition.paths[expected_tool_path]["post"]["parameters"][0]["schema"]
    assert "$ref" not in str(schema)
    assert schema["type"] == "object"
    assert "queryStr" in schema["properties"]
    assert schema["properties"]["queryStr"]["type"] == "string"

    assert danswer_tool.definition.components is None
