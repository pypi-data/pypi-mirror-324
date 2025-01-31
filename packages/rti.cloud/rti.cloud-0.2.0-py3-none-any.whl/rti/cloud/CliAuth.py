# Copyright (c) 2024 Real-Time Innovations, Inc.  All rights reserved.
# No duplications, whole or partial, manual or electronic, may be made
# without express written permission.  Any such copies, or revisions thereof,
# must display this notice unaltered.
# This code contains trade secrets of Real-Time Innovations, Inc.

import os
import time
import webbrowser

import requests


def _get_path_to_access_token_file() -> str:
    home = os.path.expanduser("~")
    return os.path.join(home, ".connext_cdb_token")


def get_access_token_from_home_file() -> str | None:
    token_file = _get_path_to_access_token_file()
    if not os.path.exists(token_file):
        return None

    with open(token_file, "r") as f:
        return f.read().strip()


def get_client_id_from_config(config: dict[str, str]) -> str | None:
    return config.get("client_id")


def get_access_token_from_auth(config: dict[str, str]) -> str | None:
    CLIENT_ID = get_client_id_from_config(config) or os.environ.get(
        "AUTH0_CLI_CLIENT_ID"
    )
    if not CLIENT_ID:
        print(
            "Error: ~/.connext_cdb_config file not found and AUTH0_CLI_CLIENT_ID not set"
        )
        return

    AUTH0_DOMAIN = "auth.rti.com"
    AUTH0_AUDIENCE = "https://cloud.rti.com/api/v1"
    # SCOPE = "openid profile email create:databus"
    SCOPE = (
        "list:databus query:databus create:databus delete:databus create:databus_client"
    )

    # Step 1: Request device and user codes
    device_code_response = requests.post(
        f"https://{AUTH0_DOMAIN}/oauth/device/code",
        data={"client_id": CLIENT_ID, "scope": SCOPE, "audience": AUTH0_AUDIENCE},
    ).json()

    device_code = device_code_response.get("device_code")
    user_code = device_code_response.get("user_code")
    verification_uri = device_code_response.get("verification_uri")
    interval = device_code_response.get("interval", 5)

    if not device_code or not user_code or not verification_uri:
        print("Error: Failed to get device code")
        return None

    if webbrowser.open(f"{verification_uri}?user_code={user_code}"):
        print(f"Authenticating at {verification_uri}?user_code={user_code})")
    else:
        print(
            f"Please open the following URL on any device to authenticate: {verification_uri}?user_code={user_code}"
        )

    # Step 3: Poll for the access token
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"

    while True:
        time.sleep(interval)
        token_response = requests.post(
            token_url,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "device_code": device_code,
                "client_id": CLIENT_ID,
            },
        )
        result = token_response.json()
        if "error" in result:
            if result["error"] == "authorization_pending":
                continue
            elif result["error"] == "slow_down":
                interval += 5
            else:
                print(f"Error: {result['error_description']}")
                break
        else:
            access_token = result["access_token"]
            break

    return access_token


def login(config: dict[str, str]) -> str | None:
    access_token = get_access_token_from_auth(config)
    if not access_token:
        return None

    # save access token
    token_file = _get_path_to_access_token_file()
    with open(token_file, "w") as f:
        f.write(access_token)

    return access_token


def logout() -> None:
    token_file = _get_path_to_access_token_file()
    if os.path.exists(token_file):
        os.remove(token_file)


def get_access_token_for_cli(config: dict[str, str]) -> str | None:
    return get_access_token_from_home_file() or login(config)
