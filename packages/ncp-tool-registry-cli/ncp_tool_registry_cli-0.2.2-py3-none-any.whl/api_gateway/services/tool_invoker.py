import logging
from typing import Optional, Dict, Any
import time
import asyncio
from functools import wraps

import aiohttp
from fastapi import Request, HTTPException
from metatron.tls import MetatronSslContext

from api_gateway.models.tool_models import ConfigBinTool
from api_gateway.services.gateway_service import replace_path_params, extract_metatron_info

logger = logging.getLogger(__name__)


def retry_with_backoff(max_attempts: int = 3, initial_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except aiohttp.ClientResponseError as e:
                    if e.status < 500 and e.status != 429:
                        raise HTTPException(status_code=e.status, detail=f"Error while invoking tool: {e.message}")
                    last_exception = e
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    last_exception = e

                if attempt < max_attempts - 1:
                    delay = initial_delay * (2**attempt)
                    logger.warning(
                        f"Request failed, retrying in {delay:.1f}s (attempt {attempt + 1}/{max_attempts})",
                        extra={"attempt": attempt + 1, "max_attempts": max_attempts, "delay": delay, "error": str(last_exception)},
                    )
                    await asyncio.sleep(delay)

            if isinstance(last_exception, aiohttp.ClientResponseError):
                raise HTTPException(
                    status_code=last_exception.status,
                    detail=f"Error during tool invocation after {max_attempts} attempts: {last_exception.message}",
                )
            elif isinstance(last_exception, aiohttp.ClientTimeout):
                raise HTTPException(status_code=504, detail=f"Request timed out after {max_attempts} attempts while invoking tool")
            else:
                raise HTTPException(
                    status_code=500, detail=f"Internal error after {max_attempts} attempts while invoking tool: {str(last_exception)}"
                )

        return wrapper

    return decorator


class ToolInvoker:
    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None

    async def initialize(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()

    async def cleanup(self):
        if self._session is None:
            return

        await self._session.close()
        self._session = None

    @retry_with_backoff()
    async def invoke_tool(self, tool: ConfigBinTool, request: Request, additional_path: str = None) -> Dict[str, Any]:
        if self._session is None:
            raise RuntimeError("Session not initialized. Call initialize() first.")

        url = tool.invocation["endpoint"]

        if additional_path:
            url = replace_path_params(url, additional_path)
            logger.info(
                "Using path params for tool %s",
                tool.tool_id,
                extra={"tool_id": tool.tool_id, "url": url, "additional_path": additional_path},
            )

        try:
            body = await request.json()
        except Exception:
            body = None

        logger.debug(
            "Request details for tool %s",
            tool.tool_id,
            extra={"tool_id": tool.tool_id, "body": body, "query_params": dict(request.query_params)},
        )

        headers = dict(request.headers)
        headers["Accept"] = "*/*"

        # # Remove hop-by-hop headers
        # hop_by_hop_headers = {
        #     "connection",
        #     "keep-alive",
        #     "proxy-authenticate",
        #     "proxy-authorization",
        #     "te",
        #     "trailers",
        #     "transfer-encoding",
        #     "upgrade",
        #     "host",
        # }
        # for header in hop_by_hop_headers:
        #     headers.pop(header.lower(), None)

        method = request.method.lower()
        logger.info(
            "Sending %s request for tool %s",
            method,
            tool.tool_id,
            extra={
                "tool_id": tool.tool_id,
                "method": method,
                "url": url,
                "is_metatron": tool.invocation.get("type") == "metatron_endpoint",
            },
        )

        ssl_context = None
        if tool.invocation.get("type") == "metatron_endpoint":
            region, env = extract_metatron_info(url)
            ssl_context = MetatronSslContext(
                appName=tool.invocation["app_name"],
                region=region,
                env=env,
            )

        timeout = aiohttp.ClientTimeout(total=15)
        tool_start_time = time.time()
        async with self._session.request(
            method=method,
            url=url,
            json=body,
            headers=headers,
            params=dict(request.query_params),
            ssl=ssl_context,
            timeout=timeout,
        ) as response:
            response.raise_for_status()

            request.state.tool_call_duration = time.time() - tool_start_time
            try:
                result = await response.json()
                logger.info(
                    "Successfully received JSON response for tool %s",
                    tool.tool_id,
                    extra={"tool_id": tool.tool_id, "response_type": "json"},
                )
                return result
            except ValueError:
                text = await response.text()
                logger.info(
                    "Successfully received text response for tool %s",
                    tool.tool_id,
                    extra={"tool_id": tool.tool_id, "response_type": "text"},
                )
                return text
