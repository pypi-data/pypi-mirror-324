from src.api_gateway.tool_registry.utils.validators import is_valid_jsonpath, is_valid_id


def test_is_valid_jsonpath():
    assert is_valid_jsonpath("$.store.book[0].title")
    assert is_valid_jsonpath("")
    assert is_valid_jsonpath(None)

    assert not is_valid_jsonpath("$.[")
    assert not is_valid_jsonpath("invalid.[")


def test_is_valid_id():
    assert is_valid_id("test123")
    assert is_valid_id("test_tool")
    assert is_valid_id("test-tool")

    assert not is_valid_id("test tool")
    assert not is_valid_id("@*$@#(!*$)()")
    assert not is_valid_id("")
