"""
some utils functions
"""

import os
from pathlib import Path
from selenium import webdriver
from azure_client.authentication import AzureAuth


AZURE_AUTH_DIRECTORY = os.path.join(Path.home(), '.azure_auth')


def create_azure_directory():
    if not os.path.isdir(AZURE_AUTH_DIRECTORY):
        os.makedirs(AZURE_AUTH_DIRECTORY)

def get_or_create_credentials(client_id, private_key, scope, tenant, redirect_uri, filename="credentials.json"):
    """
    function which gets credentials in $HOME/.azure_auth/$filename if it
    exists and regenerates a token, reauthentifies else
    """
    create_azure_directory()
    auth = AzureAuth()
    auth_path = os.path.join(AZURE_AUTH_DIRECTORY, filename)

    if not os.path.exists(auth_path):
        DriverGenerator = webdriver.Chrome
        auth.authenticate(DriverGenerator, client_id, private_key, scope, tenant, redirect_uri)
    else:
        auth.get_auth_from_file(auth_path)
        auth.refresh_access_token()
    auth.save_auth(auth_path)

    return auth
