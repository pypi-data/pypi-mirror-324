import logging
from typing import Literal
import requests

from metatron.http import MetatronAdapter

logger = logging.getLogger(__name__)


def test_get_gandalf_policy_from_ncp_project():
    def get_gandalf_policy_from_ncp_project(ncp_project_id: str, env: Literal["test", "prod"]) -> str:
        logger.info(f"Fetching Gandalf policy for NCP project {ncp_project_id} in {env}")
        url = f"https://copilotcp.cluster.us-east-1.{env}.cloud.netflix.net:7004/project/get/{ncp_project_id}"
        headers = {"accept": "application/json"}
        session = requests.Session()
        session.mount("https://", MetatronAdapter("copilotcp"))
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()
            project = response.json()
            return project["gandalf_policy_name"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching Gandalf policy: {e}")
            return None

    assert get_gandalf_policy_from_ncp_project("fassumpcaotest1", "test") == "NCP-copilot-test-fassumpcaotest1"
