import re

from jsonpath_ng import parse
from jsonpath_ng.exceptions import JsonPathLexerError, JsonPathParserError


def is_valid_jsonpath(jsonpath_string):
    if not jsonpath_string:
        return True
    try:
        parse(jsonpath_string)
        return True
    except (JsonPathLexerError, JsonPathParserError):
        return False


def is_valid_id(id):
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", id))
