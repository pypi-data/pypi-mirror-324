# Copyright (c) 2024 Real-Time Innovations, Inc.  All rights reserved.
# No duplications, whole or partial, manual or electronic, may be made
# without express written permission.  Any such copies, or revisions thereof,
# must display this notice unaltered.
# This code contains trade secrets of Real-Time Innovations, Inc.

import argparse
import json
import logging
import os
import time

import requests
from .CliAuth import get_access_token_for_cli, login, logout

#
# The UserCliApp provides a CLI interface to call the CloudDatabus REST API.
#

logger = logging.getLogger("CloudDatabusCLI")
logger.setLevel(logging.INFO)

API_DEFAULT_URL = "http://127.0.0.1:8090"
CONFIG = None
SSL_VERIFY = True


def _get_path_to_config_file() -> str:
    home = os.path.expanduser("~")
    return os.path.join(home, ".connext_cdb_config")


def _get_config_from_config_file() -> dict[str, str]:
    """Reads the configuration file (json format) and returns the configuration
    as a dictionary
    """
    config_file = _get_path_to_config_file()
    if not os.path.exists(config_file):
        return {}

    with open(config_file, "r") as f:
        return json.load(f)


def get_config() -> dict[str, str]:
    global CONFIG
    if CONFIG is None:
        CONFIG = _get_config_from_config_file()
    return CONFIG


def get_api_url() -> str:
    return get_config().get("api_host", API_DEFAULT_URL)


def get_auth_headers():
    access_token = get_access_token_for_cli(get_config())
    return {"Authorization": f"Bearer {access_token}"}


def list_databuses():
    response = requests.get(
        f"{get_api_url()}/databuses", headers=get_auth_headers(), verify=SSL_VERIFY
    )
    if response.status_code == 200:
        databuses = response.json()
        print(json.dumps(databuses, indent=2))
    else:
        print(f"Error: {response.text}")


def _query_databus(name):
    return requests.get(
        f"{get_api_url()}/databuses/{name}",
        headers=get_auth_headers(),
        verify=SSL_VERIFY,
    )


def _get_databus_status(name):
    response = _query_databus(name)
    if response.status_code == 200:
        return response.json().get("status")
    else:
        return None


def _wait_for_databus_status_change(name, previous_status):
    time.sleep(5)
    current_status = _get_databus_status(name)
    while current_status == previous_status:
        time.sleep(5)
        current_status = _get_databus_status(name)

    return current_status


def query_databus(name):
    response = _query_databus(name)
    if response.status_code == 200:
        status = response.json()
        print(json.dumps(status, indent=2))
    else:
        print(f"Error: {response.text}")


def create_databus(name, replicas, observability, system_designer, network_name):
    data = {
        "name": name,
        "replicas": replicas,
        "observability": observability,
        "system_designer": system_designer,
        "network_name": network_name,
    }
    response = requests.post(
        f"{get_api_url()}/databuses",
        headers=get_auth_headers(),
        json=data,
        verify=SSL_VERIFY,
    )
    if response.status_code == 201:
        print("Databus creation started successfully.")
    else:
        print(f"Error: {response.text}")
        return

    print("Waiting for creation to complete... (safe to Ctrl+C)")
    status = _wait_for_databus_status_change(name, "creating")

    if status is None:
        print("Failed to get databus status")
    else:
        print("Databus status: ", status)


def delete_databus(name) -> bool:
    response = requests.delete(
        f"{get_api_url()}/databuses/{name}",
        headers=get_auth_headers(),
        verify=SSL_VERIFY,
    )
    if response.status_code == 200:
        print("Databus deletion started successfully.")
    else:
        print(f"Error: {response.text}")
        return False

    print("Waiting for databus deletion to complete... (safe to Ctrl+C)")
    status = _wait_for_databus_status_change(name, "deleting")
    if status is None:
        print("Databus has been deleted")
    else:
        print("Unexpected Databus status: ", status)

    return True


def create_client_config(name, port, kind, client_name):
    data = {"port": port, "kind": kind}
    if client_name:
        data["client_name"] = client_name

    response = requests.post(
        f"{get_api_url()}/databuses/{name}/client",
        headers=get_auth_headers(),
        json=data,
        verify=SSL_VERIFY,
    )
    if response.status_code == 201:
        print(response.text)
    else:
        print(f"Error: {response.text}")


def get_client_config(name, client_name, generate_example, force_overwrite):
    response = requests.get(
        f"{get_api_url()}/databuses/{name}/client/{client_name}",
        headers=get_auth_headers(),
        verify=SSL_VERIFY,
    )
    if response.status_code == 200:
        client = response.json()
        client_config = client.get("client_config")
        if not client_config:
            print(f"Error: Unexpected client configuration for '{client_name}'")
            return

        if os.path.exists(f"{client_name}.xml") and not force_overwrite:
            print(f"{client_name}.xml already exists. Use -f to overwrite.")
        else:
            with open(f"{client_name}.xml", "w") as f:
                f.write(client_config)

            print(f'Client configuration saved in {client_name}.xml')

        if generate_example:
            client_example = client.get("client_example")
            if client_example:
                if os.path.exists(f"{client_name}.py") and not force_overwrite:
                    print(f"{client_name}.py already exists. Use -f to overwrite.")
                    return
                with open(f"{client_name}.py", "w") as f:
                    f.write(client_example)
                print(f'Client example saved in {client_name}.py')

    else:
        print(f"Error: {response.text}")


def delete_client_config(name, client_name):
    response = requests.delete(
        f"{get_api_url()}/databuses/{name}/client/{client_name}",
        headers=get_auth_headers(),
        verify=SSL_VERIFY,
    )
    if response.status_code == 200:
        print(f"Client '{client_name}' successfully deleted from databus '{name}'")
    else:
        print(f"Error: {response.text}")


# Function to add a user to a databus
def add_user_to_databus(name, email):
    response = requests.post(
        f"{get_api_url()}/databuses/{name}/users/{email}/",
        headers=get_auth_headers(),
        verify=SSL_VERIFY,
    )
    if response.status_code == 201:
        print(f"User '{email}' successfully added to databus '{name}'")
    else:
        print(f"Error adding user: {response.text}")


# Function to remove a user from a databus
def remove_user_from_databus(name, email):
    response = requests.delete(
        f"{get_api_url()}/databuses/{name}/users/{email}/",
        headers=get_auth_headers(),
        verify=SSL_VERIFY,
    )
    if response.status_code == 200:
        print(f"User '{email}' successfully removed from databus '{name}'")
    else:
        print(f"Error removing user: {response.text}")


def update_databus_status(name, status):
    data = {"running_status": status}
    response = requests.patch(
        f"{get_api_url()}/databuses/{name}",
        headers=get_auth_headers(),
        json=data,
        verify=SSL_VERIFY,
    )
    if response.status_code == 200:
        print(f"Databus '{name}' {status}d successfully.")
    else:
        print(f"Error: {response.text}")


def list_networks():
    response = requests.get(
        f"{get_api_url()}/networks", headers=get_auth_headers(), verify=SSL_VERIFY
    )
    if response.status_code == 200:
        networks = response.json()
        print(json.dumps(networks, indent=2))
    else:
        print(f"Error: {response.text}")


def delete_network(name):
    response = requests.delete(
        f"{get_api_url()}/networks/{name}",
        headers=get_auth_headers(),
        verify=SSL_VERIFY,
    )
    if response.status_code == 200:
        print(f"Network '{name}' deleted successfully.")
    else:
        print(f"Error: {response.text}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI to interact with the CloudDatabus REST API"
    )
    subparsers = parser.add_subparsers(dest="action", required=True)

    # Global option for specifying the CloudDatabus name
    name_parser = argparse.ArgumentParser(add_help=False)
    name_parser.add_argument(
        "--name", required=True, help="The name of the CloudDatabus"
    )

    common_options_parser = argparse.ArgumentParser(add_help=False)
    common_options_parser.add_argument(
        "--disable-ssl-verify",
        default=False,
        action="store_true",
        help="Disable SSL certificate verification",
    )

    # List command (does not need --name)
    subparsers.add_parser(
        "list", parents=[common_options_parser], help="List all CloudDatabuses"
    )

    # Create command (uses name_parser for --name)
    create_parser = subparsers.add_parser(
        "create",
        parents=[common_options_parser, name_parser],
        help="Create a new CloudDatabus",
    )
    create_parser.add_argument(
        "--replicas", type=int, default=2, help="The number of replicas (default: 2)"
    )
    create_parser.add_argument(
        "--observability", action="store_true", help="Enable observability features"
    )
    create_parser.add_argument(
        "--system-designer", action="store_true", help="Enable System Designer"
    )
    create_parser.add_argument(
        "--network-name",
        type=str,
        default=None,
        help="The network name for the CloudDatabus",
    )

    # Query command (uses name_parser for --name)
    subparsers.add_parser(
        "query",
        parents=[common_options_parser, name_parser],
        help="Query the status of a CloudDatabus",
    )

    # Delete command (uses name_parser for --name)
    subparsers.add_parser(
        "delete",
        parents=[common_options_parser, name_parser],
        help="Delete a CloudDatabus",
    )

    # Disable command (uses name_parser for --name)
    subparsers.add_parser(
        "disable",
        parents=[common_options_parser, name_parser],
        help="Disable a CloudDatabus",
    )

    # Resume command (uses name_parser for --name)
    subparsers.add_parser(
        "resume",
        parents=[common_options_parser, name_parser],
        help="Resume a CloudDatabus",
    )

    # Client config command (uses name_parser for --name)
    client_parser = subparsers.add_parser(
        "client",
        parents=[common_options_parser, name_parser],
        help="Create, get, or delete a client configuration for a CloudDatabus",
    )
    client_parser.add_argument(
        "--create",
        action="store_true",
        help="Create a client configuration",
    )
    client_parser.add_argument(
        "--get",
        action="store_true",
        help="Get the client configuration for the specified client name",
    )
    client_parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete the client configuration for the specified client name",
    )
    client_parser.add_argument(
        "--client-name",
        type=str,
        required=True,
        help="The name of the client",
    )
    client_parser.add_argument(
        "--port",
        type=int,
        default=7777,
        help="The port to use in the client configuration (default: 7777)",
    )
    client_parser.add_argument(
        "--kind",
        type=str,
        choices=["app", "gateway"],
        default="app",
        help="The kind of client to create (app or gateway)",
    )
    client_parser.add_argument(
        "--example",
        action="store_true",
        help="Generate the client example file",
    )
    client_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )

    # User command for adding/removing users (uses name_parser for --name)
    user_parser = subparsers.add_parser(
        "user",
        parents=[common_options_parser, name_parser],
        help="Add or remove a user to/from a CloudDatabus",
    )
    user_parser.add_argument(
        "--email",
        type=str,
        required=True,
        help="The email of the user to add or remove from the CloudDatabus",
    )
    user_parser.add_argument(
        "--add",
        action="store_true",
        help="Add the user to the CloudDatabus (default)",
        default=True,
    )
    user_parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove the user from the CloudDatabus",
        default=False,
    )

    # List networks command (does not need --name)
    subparsers.add_parser(
        "list-networks", parents=[common_options_parser], help="List all available networks"
    )

    # Delete network command (uses name_parser for --name)
    subparsers.add_parser(
        "delete-network",
        parents=[common_options_parser, name_parser],
        help="Delete a network (load balancer)",
    )

    # Login command (does not need --name)
    subparsers.add_parser("login", help="Login to the CloudDatabus service")

    # Logout command (does not need --name)
    subparsers.add_parser("logout", help="Logout of the CloudDatabus service")

    result = parser.parse_args()
    if getattr(result, "disable_ssl_verify", None):
        global SSL_VERIFY
        SSL_VERIFY = False
        print("WARNING: SSL certificate verification disabled")

    return result


def main():
    args = parse_args()

    if args.action == "list":
        list_databuses()
    elif args.action == "create":
        create_databus(
            args.name,
            args.replicas,
            args.observability,
            args.system_designer,
            args.network_name,
        )
    elif args.action == "query":
        query_databus(args.name)
    elif args.action == "delete":
        delete_databus(args.name)
    elif args.action == "disable":
        update_databus_status(args.name, "disable")
    elif args.action == "resume":
        update_databus_status(args.name, "resume")
    elif args.action == "client":
        if args.create:
            create_client_config(args.name, args.port, args.kind, args.client_name)
        elif args.get:
            get_client_config(args.name, args.client_name, args.example, args.force)
        elif args.delete:
            delete_client_config(args.name, args.client_name)
    elif args.action == "user":
        if args.remove:
            remove_user_from_databus(args.name, args.email)
        else:
            add_user_to_databus(args.name, args.email)
    elif args.action == "list-networks":
        list_networks()
    elif args.action == "delete-network":
        delete_network(args.name)
    elif args.action == "login":
        login(get_config())
    elif args.action == "logout":
        logout()
    else:
        print("Unknown action")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
