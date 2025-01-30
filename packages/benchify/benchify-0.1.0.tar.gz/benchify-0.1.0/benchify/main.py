"""
exposes the API for benchify
"""

import requests
import os
import tarfile
import typer
from urllib.parse import urlencode

from .auth import save_token, load_token, get_token_file_path
from .repo import get_repo_name_and_owner, is_benchify_initialized
from .server import start_server_in_background
from .constants import (
    CONFIG_DIR_PATH, 
    TAR_FILE_PATH, 
    AUTH_URL, 
    API_URL_GET_METADATA, 
    API_URL_CONFIG,
    Command,
    HTTPMethod
)

app = typer.Typer(help="A CLI tool for managing Benchify authentication and configuration tasks.")

def make_request(method: HTTPMethod, url: str, token: str, body: dict = None):
    """
    Make an HTTP request with the specified method, URL, token, and optional body.

    :param method: HTTP method to use (e.g., "GET", "POST", etc.)
    :param url: The URL to send the request to
    :param token: The authorization token for the request
    :param body: The request body (optional, defaults to None)
    :return: Parsed JSON response or None if parsing fails
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.request(method=method.value, url=url, headers=headers, json=body)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        response_json = response.json()  # Parse the JSON response
        return response_json
    except ValueError:
        print("Failed to parse response as JSON.")
        exit(1)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        exit(1)
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)


def generate_benchify_tar():
    try:
        with tarfile.open(TAR_FILE_PATH, "w:gz") as tar:
            tar.add(CONFIG_DIR_PATH, arcname=".")
        print("Successfully generated benchify.tar")
    except Exception as e:
        print("Failed to generate benchify.tar")
        exit(1)


def upload_to_s3(upload_url):
    try:
        with open(TAR_FILE_PATH, "rb") as f:
            headers = {'Content-Type': 'application/octet-stream'}
            response = requests.put(upload_url, data=f, headers=headers)
            if response.status_code == 200:
                os.remove(TAR_FILE_PATH)
                return True
            else:
                print("Failed to upload test configuration")
                exit(1)
    except Exception:
        print("Failed to upload test configuration")
        exit(1)


def download_and_extract_from_s3(url: str):
    # Step 1: Download the file from the S3 URL
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    
    # Step 2: Save the downloaded file as a temporary tar file
    with open(TAR_FILE_PATH, "wb") as tar_file:
        for chunk in response.iter_content(chunk_size=8192):  # Stream the file content
            tar_file.write(chunk)
    
    # Step 3: Extract the tar file to the specified output directory
    os.makedirs(CONFIG_DIR_PATH, exist_ok=True)  # Create the output directory if it doesn't exist
    with tarfile.open(TAR_FILE_PATH, "r") as tar:
        tar.extractall(path=CONFIG_DIR_PATH)
    
    # Step 4: Optionally, clean up the tar file after extraction
    os.remove(TAR_FILE_PATH)

    print(f"Files extracted to {CONFIG_DIR_PATH}")


def login():
    try:
        # Start the server in the background
        if os.path.exists(get_token_file_path()):
            print("You are already logged in.")
            exit(1)
        try:
            port, server_instance, JWTHandler = start_server_in_background()
        except Exception:
            print("Failed to start the authentication server.")
            exit(1)

        # Query parameters
        query_params = {"port": port}

        # Construct the URL
        try:
            auth_url = AUTH_URL + urlencode(query_params)
        except Exception:
            print("Failed to construct the authentication URL.")
            exit(1)

        print('On your computer or mobile device navigate to:', auth_url)
        print("Waiting for authentication...")
        # Wait for the JWT to be received with a timeout
        if not JWTHandler.jwt_received.wait(timeout=300):  # 5-minute timeout
            print("Authentication timed out. Please try again.")
            exit(1)

        jwt_value = JWTHandler.jwt_value

        # Save the token
        try:
            save_token(jwt_value)
        except Exception:
            print("Failed to save the authentication token.")
            exit(1)
        
        print("Authentication successful.")

    except Exception:
        print("An unexpected error occurred. Please try again later.")
    finally:
        # Ensure the server is shut down properly
        try:
            server_instance.shutdown()
            server_instance.server_close()
        except Exception:
            pass


def logout():
    try:
        if not os.path.exists(get_token_file_path()):
            print("You are not logged in.")
            return
        os.remove(get_token_file_path())
        print("You have successfully logged out.")
    except Exception:
        print("An unexpected error occurred. Please try again later.")
        exit(1)


def init_config():
    token = load_token()
    if not token:
        print("Please log in to proceed.")
        exit(1)
    
    if is_benchify_initialized():
        print("A Benchify configuration already exists. If you wish to reinitialize, please remove the '.benchify' directory and try again.")
        exit(1)

    owner, repo_name = get_repo_name_and_owner()
    
    print(f"Initializing Benchify for repository: {repo_name} owned by {owner}")
    print('Getting metadata...')
    metadata = get_metadata()
    print('Metadata received')
    body = {
        "runId": metadata['runId'],
        "type": "INIT"
    }
    
    print('Sending request..., this may take up to 15 minutes')
    response_json = make_request(method=HTTPMethod.POST, token=token, url=API_URL_CONFIG, body=body)

    print('Downloading configuration...')
    download_and_extract_from_s3(response_json['downloadUrl'])
    print('Benchify configuration initialized!')


def test_config():
    token = load_token()
    if not token:
        print("Please log in to proceed.")
        exit(1)
    
    if not is_benchify_initialized():
        print("No Benchify configuration found. You can initialize a new configuration by running the setup process.")
        exit(1)

    generate_benchify_tar()
    print('Getting metadata...')
    metadata = get_metadata()
    print('Metadata received')
    print('Uploading configuration...')
    upload_to_s3(metadata['uploadUrl'])

    body = {
        "runId": metadata['runId'],
        "type": "TEST"
    }
    print('Sending request..., this may take up to 15 minutes')
    # TODO: handle response and disply results to user once we have nice results.
    response_json = make_request(method=HTTPMethod.POST, token=token, url=API_URL_CONFIG, body=body)
    print('Benchify configuration tested!')


def get_metadata():
    token = load_token()
    if not token:
        print('You must first log in.')
        exit(1)
    owner, repo_name = get_repo_name_and_owner()
    body = {
        "repoOwner": owner,
        "repoName": repo_name
    }
    response_json = make_request(method=HTTPMethod.GET, token=token, url=API_URL_GET_METADATA, body=body)
    return response_json

@app.command()
def auth(command: Command):
    """
    Perform authentication tasks.

    COMMAND:
    - login: Log in to the system.
    - logout: Log out from the system.
    """
    if command == Command.LOGIN:
        login()
    elif command == Command.LOGOUT:
        logout()
    else:
        typer.echo(f"Invalid command: {command}. Use 'login' or 'logout'.")


@app.command()
def config(command: Command):
    """
    Perform configuration tasks.

    COMMAND:
    - init: Initialize the configuration.
    - test: Test the existing .benchify configuration.
    """
    if command == Command.INIT:
        init_config()
    elif command == Command.TEST:
        test_config()
    else:
        typer.echo(f"Invalid command: {command}. Use 'init' or 'test'.")

@app.command(name="init", help="Initialize the configuration (standalone command).")
def init():
    init_config()

@app.command()
def test():
    test_config()

if __name__ == "__main__":
    app()
