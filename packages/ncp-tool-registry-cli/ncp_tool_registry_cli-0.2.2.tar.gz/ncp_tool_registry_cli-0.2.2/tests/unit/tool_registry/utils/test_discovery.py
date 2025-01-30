from unittest.mock import patch, MagicMock
from src.api_gateway.tool_registry.utils import discovery


def test_get_app_name():
    assert discovery.get_app_name("https://pandora-prod-api.cluster.us-west-2.prod.cloud.netflix.net") == "pandora"
    assert discovery.get_app_name("copilotcp.cluster.us-east-1.test.cloud.netflix.net:7004") == "copilotcp"


@patch("requests.Session")
def test_discover_openapi(mock_session_class):
    base_url = "https://api.example.com"
    mock_openapi = {"openapi": "3.0.0", "paths": {"/test": {"get": {"description": "Test endpoint"}}}}

    mock_session = mock_session_class.return_value

    def get_side_effect(url):
        if url == f"{base_url}/openapi.json":
            resp = MagicMock()
            resp.ok = True
            resp.json.return_value = mock_openapi
            return resp
        resp = MagicMock()
        resp.ok = False
        return resp

    mock_session.get.side_effect = get_side_effect

    result = discovery.discover_openapi(base_url)
    assert result == mock_openapi
    assert mock_session.get.call_args_list[-1][0][0] == f"{base_url}/openapi.json"


def test_extract_refs():
    test_obj = {
        "ref1": {"$ref": "#/components/schemas/val1"},
        "ref2": {"schema": {"$ref": "#/components/schemas/val2"}},
        "ref3": [
            {
                "$ref": "#/components/schemas/val3",
            }
        ],
        "invalid": {"$ref": "not/a/valid/ref"},
        "non_ref": "regular value",
    }

    refs = discovery.extract_refs(test_obj)
    assert refs == {"val1", "val2", "val3"}


def test_get_used_components():
    path_schema = {"requestBody": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/ref1"}}}}}

    all_components = {
        "schemas": {
            "ref1": {"type": "object", "properties": {"address": {"$ref": "#/components/schemas/ref2"}}},
            "ref2": {"type": "object", "properties": {"street": {"type": "string"}}},
            "randomref": {"type": "object"},
        }
    }

    result = discovery.get_used_components(path_schema, all_components)

    assert set(result["schemas"].keys()) == {"ref1", "ref2"}
    assert result["schemas"]["ref1"] == all_components["schemas"]["ref1"]
    assert result["schemas"]["ref2"] == all_components["schemas"]["ref2"]


def test_get_endpoint_schemas_and_components():
    mock_spec = {
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get users",
                    "responses": {
                        "200": {
                            "description": "Success",
                            "content": {"application/json": {"schema": {"$ref": "#/components/schemas/UserList"}}},
                        }
                    },
                },
                "post": {
                    "summary": "Create user",
                    "requestBody": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}},
                    "responses": {"200": {"description": "Created"}},
                },
                "delete": {
                    "summary": "Delete user",
                    "requestBody": {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/User"}}}},
                    "responses": {"200": {"description": "Deleted"}},
                },
            }
        },
        "components": {
            "schemas": {
                "User": {"type": "object", "properties": {"name": {"type": "string"}}},
                "UserList": {"type": "array", "items": {"$ref": "#/components/schemas/User"}},
                "Unused": {"type": "object", "properties": {"name": {"type": "string"}}},
            }
        },
    }

    request_schemas, components, response_schemas = discovery.get_endpoint_schemas_and_components(
        path="/users", methods=["get", "post"], spec=mock_spec
    )

    assert "get" in request_schemas
    assert "post" in request_schemas
    assert "delete" not in request_schemas
    assert request_schemas["get"]["summary"] == "Get users"
    assert request_schemas["post"]["summary"] == "Create user"

    assert "User" in components["schemas"]
    assert "UserList" in components["schemas"]
    assert "Unused" not in components["schemas"]

    assert "get" in response_schemas
    assert "post" in response_schemas
    assert "delete" not in response_schemas


@patch("builtins.input", return_value="Mock summary")
def test_get_endpoint_schemas_and_components_missing_summary(mock_input):
    mock_spec = {"paths": {"/test": {"get": {"responses": {"200": {"description": "Success"}}}}}, "components": {"schemas": {}}}

    request_schemas, _, _ = discovery.get_endpoint_schemas_and_components(path="/test", methods=["get"], spec=mock_spec)

    assert request_schemas["get"]["summary"] == "Mock summary"
    mock_input.assert_called_once()
