import asyncio
import pytest
from unittest.mock import AsyncMock, Mock, patch
import aiohttp
from fastapi import Request, HTTPException

from src.api_gateway.services.tool_invoker import ToolInvoker
from src.api_gateway.models.tool_models import ConfigBinTool, Permissions, GenAIProject, Info


@pytest.fixture
def tool_invoker():
    return ToolInvoker()


@pytest.fixture
def mock_request():
    request = Mock(spec=Request)
    request.method = "GET"
    request.headers = {}
    request.query_params = {}
    request.state = Mock()
    return request


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
        invocation={"endpoint": "http://test.com"},
        components={},
    )


@pytest.fixture
def request_info():
    info = Mock()
    info.real_url = "http://test.com"
    return info


@pytest.fixture
def mock_success_response():
    response = Mock()
    response.raise_for_status = Mock()
    response.json = AsyncMock(return_value={"success": True})
    return response


@pytest.fixture
def mock_session_context(mock_success_response):
    return AsyncMock(__aenter__=AsyncMock(return_value=mock_success_response), __aexit__=AsyncMock(return_value=None))


async def run_test_with_retries(tool_invoker, mock_request, mock_tool, side_effects, expected_calls=3):
    with patch("aiohttp.ClientSession") as MockSession:
        mock_session = Mock()
        mock_session.close = AsyncMock()
        MockSession.return_value = mock_session
        mock_session.request = Mock(side_effect=side_effects)

        await tool_invoker.initialize()
        try:
            result = await tool_invoker.invoke_tool(mock_tool, mock_request)
            assert result == {"success": True}
        except HTTPException as e:
            return e
        finally:
            assert mock_session.request.call_count == expected_calls
            await tool_invoker.cleanup()


@pytest.mark.asyncio
async def test_retry_on_server_error(tool_invoker, mock_request, mock_tool, request_info, mock_session_context):
    side_effects = [
        aiohttp.ClientResponseError(request_info, (), status=503),
        aiohttp.ClientResponseError(request_info, (), status=503),
        mock_session_context,
    ]
    await run_test_with_retries(tool_invoker, mock_request, mock_tool, side_effects)


@pytest.mark.asyncio
async def test_no_retry_on_client_error(tool_invoker, mock_request, mock_tool, request_info):
    error = aiohttp.ClientResponseError(request_info, (), status=400)

    with patch("aiohttp.ClientSession") as MockSession:
        mock_session = Mock()
        mock_session.close = AsyncMock()
        MockSession.return_value = mock_session
        mock_session.request = Mock(side_effect=[error])

        await tool_invoker.initialize()
        with pytest.raises(HTTPException) as exc_info:
            await tool_invoker.invoke_tool(mock_tool, mock_request)

        assert exc_info.value.status_code == 400
        assert mock_session.request.call_count == 1


@pytest.mark.asyncio
async def test_exponential_backoff(tool_invoker, mock_request, mock_tool, request_info, mock_session_context):
    with patch("asyncio.sleep") as mock_sleep:
        side_effects = [
            aiohttp.ClientResponseError(request_info, (), status=503),
            aiohttp.ClientResponseError(request_info, (), status=503),
            mock_session_context,
        ]
        await run_test_with_retries(tool_invoker, mock_request, mock_tool, side_effects)

        assert mock_sleep.call_count == 2
        assert mock_sleep.call_args_list[0][0][0] == 1.0
        assert mock_sleep.call_args_list[1][0][0] == 2.0


@pytest.mark.asyncio
async def test_retry_on_timeout(tool_invoker, mock_request, mock_tool, mock_session_context):
    side_effects = [asyncio.TimeoutError(), asyncio.TimeoutError(), mock_session_context]
    await run_test_with_retries(tool_invoker, mock_request, mock_tool, side_effects)


@pytest.mark.asyncio
async def test_retry_on_rate_limit(tool_invoker, mock_request, mock_tool, request_info, mock_session_context):
    side_effects = [
        aiohttp.ClientResponseError(request_info, (), status=429),
        aiohttp.ClientResponseError(request_info, (), status=429),
        mock_session_context,
    ]
    await run_test_with_retries(tool_invoker, mock_request, mock_tool, side_effects)


@pytest.mark.asyncio
async def test_max_retries_exceeded(tool_invoker, mock_request, mock_tool, request_info):
    error = aiohttp.ClientResponseError(request_info, (), status=503)
    exc = await run_test_with_retries(tool_invoker, mock_request, mock_tool, error)

    assert exc.status_code == 503
    assert "after 3 attempts" in str(exc.detail)
