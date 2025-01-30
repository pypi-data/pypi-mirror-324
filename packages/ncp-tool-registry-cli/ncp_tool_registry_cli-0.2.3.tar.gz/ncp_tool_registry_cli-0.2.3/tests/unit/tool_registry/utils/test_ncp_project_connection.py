from src.api_gateway.tool_registry.utils.ncp_project_connection import get_gandalf_policy_from_ncp_project


def test_get_gandalf_policy_from_ncp_project():
    assert get_gandalf_policy_from_ncp_project("fassumpcaotest1", "test") == "NCP-copilot-test-fassumpcaotest1"
