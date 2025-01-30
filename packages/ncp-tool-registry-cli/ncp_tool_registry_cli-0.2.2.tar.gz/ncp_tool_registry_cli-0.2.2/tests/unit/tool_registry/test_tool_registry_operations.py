import pytest
from unittest.mock import patch, MagicMock

from src.api_gateway.tool_registry.tool_registry_operations import ToolRegistryOperations
from src.api_gateway.models.tool_models import CreateToolRequest, Info, CreateToolRequestGenAIProject


@pytest.fixture
def registry():
    configbin_manager_mock = MagicMock()
    danswer_manager_mock = MagicMock()
    configbin_manager_mock.get_tool_by_id.return_value = None
    return ToolRegistryOperations(configbin_manager=configbin_manager_mock, danswer_manager=danswer_manager_mock)


@pytest.fixture
def valid_tool_request():
    return CreateToolRequest(
        base_url="http://api.example.com",
        owner=CreateToolRequestGenAIProject(env="test", project_id="test"),
        path="/path",
        methods=["GET"],
        info=Info(title="Test Tool", description="Test Description", version="1.0.0"),
    )


@pytest.fixture
def mock_get_gandalf_policy():
    with patch("src.api_gateway.tool_registry.tool_registry_operations.get_gandalf_policy_from_ncp_project") as mock_get_gandalf_policy:
        mock_get_gandalf_policy.return_value = "test_policy"
        yield mock_get_gandalf_policy


@pytest.fixture
def mock_discover():
    with patch("src.api_gateway.tool_registry.tool_registry_operations.discover_openapi") as mock_discover:
        mock_discover.return_value = {
            "openapi": "3.0.0",
            "paths": {
                "/users": {
                    "get": {
                        "summary": "Get users",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "data": {"type": "object", "properties": {"user": {"type": "string"}}},
                                            "metadata": {"type": "string"},
                                        },
                                    }
                                }
                            }
                        },
                    }
                }
            },
        }
        yield mock_discover


@pytest.fixture
def mock_get_schemas():
    with patch("src.api_gateway.tool_registry.tool_registry_operations.get_endpoint_schemas_and_components") as mock_get_schemas:
        mock_get_schemas.return_value = (
            {
                "get": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"type": "object", "properties": {"metadata": {"type": "string"}, "data": {"type": "string"}}}
                            },
                            "application/xml": {"schema": {"type": "object", "properties": {"metadata": {"type": "string"}}}},
                        }
                    }
                }
            },
            {},  # components
            {},  # response_schemas
        )
        yield mock_get_schemas


def test_register_tool_invalid_id(registry, valid_tool_request):
    with pytest.raises(ValueError, match="Invalid tool_id! Please use only alphanumeric characters, underscores, and dashes"):
        registry.register_tool("invalid@id!", valid_tool_request)


def test_register_tool_no_gandalf_policy(registry, valid_tool_request, mock_get_gandalf_policy):
    mock_get_gandalf_policy.return_value = None
    with pytest.raises(ValueError, match="Could not fetch Gandalf policy for given owner NCP project id and env."):
        registry.register_tool("valid_id", valid_tool_request)


def test_register_tool_no_openapi_spec(registry, valid_tool_request, mock_get_gandalf_policy):
    valid_tool_request.base_url = "http://randomurlwithnodocs3929039210.com"
    with pytest.raises(ValueError, match="Could not find OpenAPI docs for provided URL"):
        registry.register_tool("valid_id", valid_tool_request)


def test_register_tool_invalid_preprocessing_jsonpath_syntax(
    registry, valid_tool_request, mock_get_gandalf_policy, mock_discover, mock_get_schemas
):
    valid_tool_request.preprocessing_jsonpath = "$.invalid[path"
    with pytest.raises(ValueError, match="Invalid preprocessing_jsonpath"):
        registry.register_tool("valid_id", valid_tool_request)


def test_register_tool_preprocessing_jsonpath_non_dict_result(
    registry, valid_tool_request, mock_get_gandalf_policy, mock_discover, mock_get_schemas
):
    valid_tool_request.preprocessing_jsonpath = "$..properties.metadata"  # This returns mulitple matches (list result)

    with pytest.raises(ValueError, match="Invalid preprocessing_jsonpath"):
        registry.register_tool("valid_id", valid_tool_request)


def test_register_tool_invalid_postprocessing_path(registry, valid_tool_request, mock_get_gandalf_policy, mock_discover, mock_get_schemas):
    valid_tool_request.postprocessing_jsonpath = "invalid[json.path"
    with pytest.raises(ValueError, match="Invalid postprocessing_jsonpath"):
        registry.register_tool("valid_id", valid_tool_request)


def test_register_tool_success(registry, valid_tool_request, mock_get_gandalf_policy, mock_discover, mock_get_schemas):
    registry.configbin_manager.add_tool_to_configbin = MagicMock()
    registry.danswer_manager.add_single_tool = MagicMock()

    tool = registry.register_tool("valid_id", valid_tool_request)

    assert tool.tool_id == "valid_id"
    assert tool.openapi == "3.0.0"
    assert registry.configbin_manager.add_tool_to_configbin.called
    assert registry.danswer_manager.add_single_tool.called
