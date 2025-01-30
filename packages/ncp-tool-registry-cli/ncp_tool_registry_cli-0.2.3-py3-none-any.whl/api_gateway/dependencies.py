from fastapi import FastAPI, Request, Depends

from api_gateway.services.tool_invoker import ToolInvoker


def get_app(request: Request):
    return request.app


async def get_configbin_manager(app: FastAPI = Depends(get_app)):
    return app.state.configbin_manager


async def get_metrics_client(app: FastAPI = Depends(get_app)):
    return app.state.tool_invocation_metrics_client


async def get_tool_registry_ops(
    app: FastAPI = Depends(get_app),
):
    return app.state.tool_registry_ops


async def get_tool_invoker(app: FastAPI = Depends(get_app)) -> ToolInvoker:
    return app.state.tool_invoker
