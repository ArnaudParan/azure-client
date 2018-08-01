"""
Module which handles the outlook email REST API
"""

import json
import urllib.request
import urllib.error
from azure_client.exceptions import AzureError


def create_draft(auth, subject, body, addresses, user_id):
    """
    this functions creates a draft with the email data given
    the user id should be either 'me', either 'users/email@domain.com'
    either 'users/{AAD_userId@AAD_tenandId}',
    see https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/use-outlook-rest-api#target-user
    for more
    """
    data = {}
    data['subject'] = subject
    data['body'] = {}
    data['body']['contentType'] = 'HTML'
    data['body']['content'] = body
    data['toRecipients'] = [{'emailAddress': {'address': addr}} for addr in addresses]

    params = json.dumps(data).encode('utf8')

    url = "https://graph.microsoft.com/beta/{}/messages".format(user_id)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(auth.access_token)
        }
    req = urllib.request.Request(url, params, headers)
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as err:
        raise AzureError(err)
