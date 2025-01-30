import json


# Stolen from https://github.netflix.net/corp/ncp-copilot-dp-python/blob/main/tests/test_gandalf.py


def get_user(user_email):
    return json.dumps(
        {
            "enforcementMode": "ENFORCE_ALL",
            "direct": {
                "authSource": "METATRON",
                "userAuthorizableIdentity": {
                    "username": user_email,
                    "domain": "netflix.com",
                },
            },
        }
    )


def get_app(app_name, user_email):
    return json.dumps(
        {
            "enforcementMode": "ENFORCE_ALL",
            "direct": {
                "authSource": "METATRON",
                "appAuthorizableIdentity": {
                    "accountId": "635200943224",
                    "applicationName": app_name,
                    "originUser": {
                        "username": "rleung@netflix.com",
                        "domain": "netflix.com",
                    },
                },
            },
            "initial": {
                "authSource": "MEECHUM_TOKEN",
                "userAuthorizableIdentity": {
                    "username": user_email,
                    "domain": "netflix.com",
                },
            },
        }
    )


# def test_laptop_user_approved():
#     assert is_authorized(get_user("dleen@netflix.com"), "NCP-copilot-dev-allow-team")
#     assert not authorize(get_user("joe@netflix.com"), "NCP-copilot-dev-allow-team")


# def test_notebook_app_denied():
#     # The user alone is authorized
#     assert authorize(get_user("dleen@netflix.com"), "NCP-copilot-integration-test-application-denied")
#     # But not when calling from a notebook as the notebook spinnaker app is not authorized
#     assert not authorize(
#         get_app("bdpnotebook", "dleen@netflix.com"), "NCP-copilot-integration-test-application-denied"
#     )
