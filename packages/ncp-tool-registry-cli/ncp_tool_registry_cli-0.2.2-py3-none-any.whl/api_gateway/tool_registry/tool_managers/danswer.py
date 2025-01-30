import base64
from typing import Dict, Any
import requests
from requests import HTTPError
import copy
import logging

import jsonref
from metatron.http import MetatronAdapter
from metatron.decrypt import MetatronDecryptor
import nflxenv

from api_gateway.models.tool_models import ConfigBinTool, DanswerTool, DanswerToolDefinition, Info, CustomHeader
from api_gateway.tool_registry.tool_managers.configbin import get_tool_invocation_path

logger = logging.getLogger(__name__)


class DanswerToolManager:
    def __init__(self, env: str = nflxenv.nf_env("test")):
        self.env = env
        self.base_url = f"https://nflxdanswerdeployment.vip.us-east-1.{env}.cloud.netflix.net:7004"

        self.session = requests.Session()
        self.session.mount("https://", MetatronAdapter("nflxdanswerdeployment"))

        if env == "prod":
            self.app_name = "Danswer"
            encrypted_secret = "TVROMThhCAESIQMwXwicuHDsP6d3gSFgTtc934XklXLHifaISWcLgEkoSxoFCLWgnQEinwIKo03d/xjKS5W9BPP6u/ALGb4rj4nGzRK2qCurtGV8hZhWnTE2BBylV7uNrnCJmA8asyIixr3XwRiF+oQkasFNnQEbdFkBw5O5n4GVHyuvGL9tPuUuXCAVYyiE0MUqQnUEZ8brDfrrjTv/FG9H//75NE62n8Xb96ZW9Fmw9i6+D+iG7zP0Il1OyI7GxesWO+/J/TcJrt45mqiIHwfNTJhhkRkSsHkMTtjumhdzNBCSAXKhDSSm1CpZVN5/0DpdLU+XHo/zqmtKTu9LipLeRWMkQI89Z0RevpWOXPZse59F0y7rA6rvxVaPOrinxYe2+TJuRFKBYgCBkRylbE0u2cOcpevBh3q4sfwpqKkqFOjM/kQ0tKa58CHdGUMhLs+gdw=="
        else:
            self.app_name = "Onyx"
            encrypted_secret = "TVROMThhCAESIQIzZApLgiQaUFHOqF+g9NYycCT2qfvUbHjgxSTLddCPGRoFCLWgnQEinwJsM8M+7ccfbX6WAC/AoIS6dM45fNBod3/6p2xE2p/1SNuN65C2wSYKzuLbLlDm3q5T+hfK+FquMM5UQYIMzpPapE3f7f8j6MIC+38PS/NOhkkG0sDwS7jFmLV9RMoqZ6n9ZD0Rlbw4tvf9cs6NqFZWyatjfjJcUdKXlmFHvmdBLW2qs15hNBMbRHyOUpbUfo8wzZ0d2m92kGFqRO4DBbRseYIAykaAk1ixaLxYpRAfV+M9XFREiKddpSBDGYUCr2zM+cU45U61/j9FPpKyhHk0qOiqKRJBskYISNd7D4xHTYtNtNrEjaTrGdErVGxb06uUSq7ENF7f+XVIIFfa3Gjo8+R5Uh1O6BkbinL/lNh/rKWHtVhr43/8sHntR1kJHw=="
        ciphertext = base64.b64decode(encrypted_secret)
        plaintext = MetatronDecryptor().decryptBytes(ciphertext)
        self.api_key = plaintext.decode("utf-8")

    def is_tool_present(self, tool_title: str) -> bool:
        response = self.session.get(f"{self.base_url}/api/tool", headers={f"X-{self.app_name}-Authorization": f"Bearer {self.api_key}"})
        response.raise_for_status()
        tools = response.json()
        for tool in tools:
            if tool["name"] == tool_title:
                return True
        return False

    def _add_custom_tool(self, tool_schema: Dict[str, Any]):
        response = self.session.post(
            f"{self.base_url}/api/admin/tool/custom",
            json=tool_schema,
            headers={f"X-{self.app_name}-Authorization": f"Bearer {self.api_key}"},
        )
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(http_err.response.text)
            raise
        return response.json()

    def add_single_tool(self, tool: ConfigBinTool) -> bool:
        try:
            if not self.is_tool_present(tool.info.title):
                danswer_schema = self.translate_configbin_tool_to_danswer(tool, self.env)
                self._add_custom_tool(danswer_schema.model_dump(exclude_none=True))
                logger.info(f"Added tool {tool.tool_id} to Danswer")
                return True
            else:
                logger.warning(f"Tool {tool.tool_id} already present in Danswer")
                return False
        except Exception as e:
            logger.error(f"Failed to add tool {tool.tool_id} to Danswer: {e}")
            raise e

    @staticmethod
    def translate_configbin_tool_to_danswer(configbin_tool: ConfigBinTool, env: str) -> DanswerTool:
        definition = DanswerToolDefinition(
            info=Info(title=configbin_tool.info.title, description=configbin_tool.info.description, version=configbin_tool.info.version),
            openapi=configbin_tool.openapi,
            paths={get_tool_invocation_path(configbin_tool): configbin_tool.request_schema},
            components=configbin_tool.components,
        )
        dereferenced_definition = jsonref.replace_refs(definition.model_dump())
        dereferenced_definition = copy.deepcopy(dereferenced_definition)
        dereferenced_definition["components"] = None

        return DanswerTool(
            name=configbin_tool.info.title,
            description=configbin_tool.info.description,
            definition=DanswerToolDefinition.model_validate(dereferenced_definition),
            custom_headers=[
                CustomHeader(key="Host", value=f"p7004.apigateway.vip.us-east-1.{env}.dns.mesh.netflix.net"),
                CustomHeader(key="Content-Type", value="application/json"),
            ],
        )

    def _delete_tool_by_danswer_id(self, danswer_tool_id: int):
        response = self.session.delete(
            f"{self.base_url}/api/admin/tool/custom/{danswer_tool_id}",
            headers={f"X-{self.app_name}-Authorization": f"Bearer {self.api_key}"},
        )
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(http_err.response.text)
            raise
        logger.info(f"Deleted tool {danswer_tool_id} from Danswer")
        return response.json()

    def delete_tool(self, tool_title: str) -> bool:
        response = self.session.get(f"{self.base_url}/api/tool", headers={f"X-{self.app_name}-Authorization": f"Bearer {self.api_key}"})
        tools = response.json()
        for tool in tools:
            if tool["name"] == tool_title:
                self._delete_tool_by_danswer_id(tool["id"])
                return True
        logger.warning(f"Tool {tool_title} not found in Danswer")
        return False

    def _update_tool_by_danswer_id(self, danswer_tool_id: int, tool_schema: Dict[str, Any]):
        response = self.session.put(
            f"{self.base_url}/api/admin/tool/custom/{danswer_tool_id}",
            json=tool_schema,
            headers={"X-Danswer-Authorization": f"Bearer {self.api_key}"},
        )
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            logger.error(http_err.response.text)
            raise
        return response.json()

    def update_tool(self, old_title: str, updated_tool: ConfigBinTool) -> bool:
        try:
            response = self.session.get(
                f"{self.base_url}/api/tool", headers={f"X-{self.app_name}-Authorization": f"Bearer {self.api_key2}"}
            )
            tools = response.json()
            for tool in tools:
                if tool["name"] == old_title:
                    danswer_schema = self.translate_configbin_tool_to_danswer(updated_tool, self.env)
                    self._update_tool_by_danswer_id(tool["id"], danswer_schema.model_dump(exclude_none=True))
                    logger.info(f"Updated tool {old_title} in Danswer")
                    return True

            logger.warning(f"Tool {old_title} not found in Danswer")
            return False
        except Exception as e:
            logger.error(f"Failed to update tool {old_title} in Danswer: {e}")
            return False
