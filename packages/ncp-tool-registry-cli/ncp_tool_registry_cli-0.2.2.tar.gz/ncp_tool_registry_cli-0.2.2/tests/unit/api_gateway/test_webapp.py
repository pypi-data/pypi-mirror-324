import pytest

from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, Mock, MagicMock
from nflx_security_util.testing import AppCallerTestClient, UserCallerTestClient

from api_gateway.tool_registry.tool_registry_operations import ToolRegistryOperations
from src.api_gateway.webapp import APP
from src.api_gateway.models.tool_models import ConfigBinTool, Info, Permissions, GenAIProject


@pytest.fixture
def mock_tool():
    return ConfigBinTool(
        tool_id="test-tool",
        permissions=Permissions(
            owner=GenAIProject(env="test", project_id="test", gandalf_policy="test"),
            accessibility="public",
            allowed_projects=[],
        ),
        response_schema={},
        openapi="3.1.0",
        info=Info(title="Test Tool", description="Test Description", version="1.0.0"),
        request_schema={},
        invocation={"endpoint": "https://api.example.com/v1/test", "type": "hi"},
        components={},
    )


@pytest.fixture
def mock_configbin_manager(mock_tool):
    manager = MagicMock()
    manager.get_tool_by_id = Mock(side_effect=lambda x: mock_tool if x == "test-tool" else None)
    return manager


@pytest.fixture
def test_client(mock_configbin_manager):
    mock_metrics_client = MagicMock()
    mock_danswer_manager = MagicMock()
    mock_tool_invoker = MagicMock()
    mock_tool_invoker.invoke_tool = AsyncMock()

    APP.state.configbin_manager = mock_configbin_manager
    APP.state.danswer_manager = mock_danswer_manager
    APP.state.tool_registry_ops = ToolRegistryOperations(mock_configbin_manager, mock_danswer_manager)
    APP.state.tool_invocation_metrics_client = mock_metrics_client
    APP.state.tool_invoker = mock_tool_invoker

    APP.state.tool_invocation_metrics_client.cleanup = AsyncMock()
    APP.state.tool_invoker.cleanup = AsyncMock()

    client = TestClient(APP)
    yield client


def test_tool_not_found(test_client):
    response = test_client.post("/ncp_model_gateway/v1/function/nonexistent/invoke")
    assert response.status_code == 404
    assert "Tool not found" in response.json()["detail"]


def test_successful_invocation_json(test_client):
    mock_response = {"result": "Success"}
    test_client.app.state.tool_invoker.invoke_tool.return_value = mock_response

    response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke")

    assert response.status_code == 200
    assert response.json() == {"result": "Success"}
    test_client.app.state.tool_invoker.invoke_tool.assert_called_once()


def test_successful_invocation_text(test_client):
    mock_response = "Success"
    test_client.app.state.tool_invoker.invoke_tool.return_value = mock_response

    response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke")

    assert response.status_code == 200
    assert response.json() == "Success"
    test_client.app.state.tool_invoker.invoke_tool.assert_called_once()


def test_invocation_with_path(test_client):
    mock_response = {"key": "value"}
    test_client.app.state.tool_invoker.invoke_tool.return_value = mock_response

    response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke/additional/path")

    assert response.status_code == 200
    test_client.app.state.tool_invoker.invoke_tool.assert_called_once()
    call_kwargs = test_client.app.state.tool_invoker.invoke_tool.call_args[1]
    assert call_kwargs["additional_path"] == "additional/path"


def test_postprocessing(test_client, mock_tool):
    mock_tool.postprocessing_jsonpath = "$.data"
    mock_response = {"data": {"key": "value"}}
    test_client.app.state.tool_invoker.invoke_tool.return_value = mock_response

    response = test_client.post("/ncp_model_gateway/v1/function/test-tool/invoke")

    assert response.status_code == 200
    test_client.app.state.tool_invoker.invoke_tool.assert_called_once()
    assert response.json() == {"key": "value"}


def test_protected():
    user_test_client = UserCallerTestClient(APP, username="test@netflix.com")
    rv = user_test_client.get("/protected")
    assert rv.status_code == 200
    assert rv.json() == "Email: test@netflix.com"

    app_test_client = AppCallerTestClient(APP, applicationName="testapp")
    rv = app_test_client.get("/protected")
    assert rv.status_code == 200
    assert rv.json() == "Application Name: testapp"


def test_healthcheck(test_client):
    rv = test_client.get("/healthcheck")
    assert rv.status_code == 200
    assert rv.headers["content-type"] == "application/json"
    assert rv.json() == "OK"
