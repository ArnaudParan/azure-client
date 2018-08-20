"""
Module which handles the outlook email REST API
"""

import logging
import json
import urllib.request
import urllib.error
from azure_client.exceptions import AzureError


def create_draft(auth, subject, body, addresses, user_id, cc_addresses=[], attachments_list=None):
    """
    this functions creates a draft with the email data given
    the user id should be either 'me', either 'users/email@domain.com'
    either 'users/{AAD_userId@AAD_tenandId}',
    see https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/use-outlook-rest-api#target-user
    for more
    """
    data = {}
    data['Subject'] = subject
    data['Body'] = {}
    data['Body']['ContentType'] = 'HTML'
    data['Body']['Content'] = body
    data['ToRecipients'] = [{'EmailAddress': {'Address': addr}} for addr in addresses]
    data['ccRecipients'] = [{'EmailAddress': {'Address': addr}} for addr in cc_addresses]
    if attachments_list is not None:
        data['Attachments'] = attachments_list

    params = json.dumps(data).encode('utf8')

    url = "https://graph.microsoft.com/beta/{}/messages".format(user_id)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(auth.access_token)
        }
    req = urllib.request.Request(url, params, headers)
    try:
        resp = urllib.request.urlopen(req)
        resp_data = json.load(resp)

        logging.getLogger(__name__).info("Draft created")

        return resp_data['id']
    except urllib.error.HTTPError as err:
        raise AzureError(err)
