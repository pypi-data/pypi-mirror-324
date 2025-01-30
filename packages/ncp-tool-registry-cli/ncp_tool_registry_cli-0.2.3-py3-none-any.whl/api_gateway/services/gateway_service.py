import re
import time
from typing import Tuple

from fastapi import Request
from spectator import GlobalRegistry
from urllib.parse import urlparse
import jsonpath_ng


def replace_path_params(url, param_values):
    values = param_values.split("/")

    result = url
    value_index = 0
    start = 0

    while True:
        start = result.find("{", start)
        if start == -1 or value_index >= len(values):
            break

        end = result.find("}", start)
        if end == -1:
            break

        result = result[:start] + values[value_index] + result[end + 1 :]
        value_index += 1

    return result


def process_schema(schema, path_expression):
    try:
        jsonpath_expr = jsonpath_ng.parse(path_expression)
        matches = jsonpath_expr.find(schema)

        if not matches:
            return None

        if len(matches) == 1:
            return matches[0].value

        return [match.value for match in matches]
    except Exception:
        return None


def extract_metatron_info(endpoint: str) -> Tuple[str, str]:
    parsed = urlparse(endpoint)

    pattern = r".*\.([a-z]+-[a-z]+-\d+)\.([a-z]+)\..*\.netflix\.net"
    match = re.match(pattern, parsed.hostname)

    if match:
        region, env = match.groups()
        return region, env

    return "us-east-1", "test"  # default values


def log_latencies_to_atlas(request: Request, tool_id: str, postprocessing: str = "false", error: str = "None"):
    total_duration = time.time() - request.state.start_time
    tool_call_duration = getattr(request.state, "tool_call_duration", 0)

    GlobalRegistry.pct_timer(
        "apigateway.overheadLatency", tags={"tool_id": tool_id, "postprocessing": postprocessing, "error": error}
    ).record(total_duration - tool_call_duration)
    GlobalRegistry.pct_timer("apigateway.toolInvocationLatency", tags={"tool_id": tool_id, "error": error}).record(tool_call_duration)
    GlobalRegistry.pct_timer("apigateway.e2eLatency", tags={"tool_id": tool_id, "postprocessing": postprocessing, "error": error}).record(
        total_duration
    )
