from pydantic import BaseModel

# class CallerMetric(BaseModel):
#     timestamp: datetime
#     username: str
#     app_name: str | None
#     auth_source: str
#     success: bool
#     error: str | None


class ToolInvocationMetric(BaseModel):
    timestamp: str | None = None
    tool_id: str | None = None
    username: str | None = None
    app_name: str | None = None
    project_id: str | None = None
    accessibility: str | None = None
    auth_source: str | None = None
    success: bool = True
    error: str | None = None
