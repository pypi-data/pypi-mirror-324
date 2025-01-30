from enum import Enum
from pydantic import BaseModel
from typing import Dict, Any, List, Literal, Optional


class HTTPMethod(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"

    @classmethod
    def _missing_(cls, value):
        value = str(value).lower()
        for member in cls:
            if member.value == value:
                return member


class Info(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None


class GenAIProject(BaseModel):
    env: Literal["test", "prod"]
    project_id: str
    gandalf_policy: str


class Permissions(BaseModel):
    owner: GenAIProject
    accessibility: Optional[Literal["public", "protected"]] = "public"
    allowed_projects: Optional[List[GenAIProject]] = []


class ConfigBinTool(BaseModel):
    tool_id: str
    info: Info
    openapi: str
    permissions: Permissions
    invocation: Dict[str, Any]
    request_schema: Dict[HTTPMethod, Dict[str, Any]]
    preprocessing_jsonpath: Optional[str] = ""
    response_schema: Dict[str, Any]
    postprocessing_jsonpath: Optional[str] = ""
    components: Optional[Dict[str, Any]] = {}


class Server(BaseModel):
    url: str = "http://host.docker.internal:4321"
    description: Optional[str] = None


class CustomHeader(BaseModel):
    key: str
    value: str


class DanswerToolDefinition(BaseModel):
    info: Info
    openapi: str
    paths: Dict[str, Any]
    components: Dict[str, Any] | None
    servers: List[Server] = [Server()]  # Default server above


class DanswerTool(BaseModel):
    name: str
    description: str
    definition: DanswerToolDefinition
    custom_headers: List[CustomHeader] = [
        CustomHeader(key="Host", value="p7004.apigateway.vip.us-east-1.test.dns.mesh.netflix.net"),
        CustomHeader(key="Content-Type", value="application/json"),
    ]
    passthrough_auth: bool = True


class CreateToolRequestGenAIProject(BaseModel):
    env: Literal["test", "prod"]
    project_id: str


class CreateToolRequest(BaseModel):
    info: Info
    owner: CreateToolRequestGenAIProject
    accessibility: Optional[Literal["public", "protected"]] = "public"
    allowed_projects: Optional[List[CreateToolRequestGenAIProject]] = []
    base_url: str
    path: str
    methods: List[HTTPMethod]
    preprocessing_jsonpath: Optional[str] = None
    postprocessing_jsonpath: Optional[str] = None


class RegistryTool(BaseModel):
    tool_id: str
    info: Info
    openapi: str
    permissions: Permissions
    invocation: Dict[str, Any]
    request_schema: Dict[HTTPMethod, Dict[str, Any]]
    preprocessing_jsonpath: Optional[str] = ""
    response_schema: Dict[str, Any]
    postprocessing_jsonpath: Optional[str] = ""
    components: Optional[Dict[str, Any]] = {}


class UpdateToolRequest(BaseModel):
    info: Optional[Info] = None
    openapi: Optional[str] = None
    permissions: Optional[Permissions] = None
    invocation: Optional[Dict[str, Any]] = None
    request_schema: Optional[Dict[HTTPMethod, Dict[str, Any]]] = None
    preprocessing_jsonpath: Optional[str] = None
    response_schema: Optional[Dict[str, Any]] = None
    postprocessing_jsonpath: Optional[str] = None
    components: Optional[Dict[str, Any]] = None


# This is in case people want to reconfigure a tool with the same tool_id.
# It only requires the "basic" info needed to create a tool, instead of all the schemas, components, etc.
class ReconfigureToolRequest(CreateToolRequest):
    pass


class Version(BaseModel):
    user: str
    comment: str
    hash: str
    prefixVersion: int
    ts: int


class ConfigBinToolConfig(BaseModel):
    name: str
    payload: ConfigBinTool
    version: Version
