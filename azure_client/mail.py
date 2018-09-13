"""
Module which handles the outlook email REST API
"""

import logging
import json
import urllib.request
import urllib.error
from azure_client.exceptions import AzureError


API_URL = "https://graph.microsoft.com/beta"


def create_draft(auth, subject, body, addresses, user_id, cc_addresses=[], attachments_list=None):
    """
    this functions creates a draft with the email data given
    the user id should be either 'me', either 'users/email@domain.com'
    either 'users/{AAD_userId@AAD_tenandId}',
    see https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/use-outlook-rest-api#target-user
    for more

    Args:
        auth (azure_client.authentication.AzureAuth): authentication object with credentials
        subject (str): the subject of the message
        body (str): the body of the message in html
        addresses (list): the list of the addresses of the recipients
        user_id (str): the id of the user, either 'me' or 'users/email@domain.com'
        cc_addresses (list): a list of the addresses to cc
        attachments_list (list): a list formatted as described here
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/mail-rest-operations#create-attachments
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

    url = "{api_url}/{user_id}/messages".format(api_url=API_URL, user_id=user_id)

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

def get_emails(auth, user_id, folder_id='AllItems', selector=[]):
    """
    implementation of that endpoint:
    https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/mail-rest-operations#get-messages

    Args:
        auth (azure_client.authentication.AzureAuth): authentication object with credentials
        user_id (str): the id of the user, either 'me' or 'users/email@domain.com'
        folder_id (str): either the id of the folder or 'Inbox' 'Drafts' 'SentItems' 'DeletedItems'
            by default 'AllItems'
        selector (list): a list of all the elements you want to select
    """
    url = "{api_url}/{user_id}/MailFolders/{folder_id}/messages?$select={selector}".format(
        api_url=API_URL,
        user_id=user_id,
        folder_id=folder_id,
        selector=','.join(selector)
        )

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(auth.access_token)
        }

    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        resp_data = json.load(resp)

        logging.getLogger(__name__).info("Messages recieved")

        return resp_data['value']
    except urllib.error.HTTPError as err:
        raise AzureError(err)

def send_email(auth, user_id, message_id):
    """
    implementation of that endpoint:
    https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/mail-rest-operations#send-a-draft-message

    Args:
        auth (azure_client.authentication.AzureAuth): authentication object with credentials
        user_id (str): the id of the user, either 'me' or 'users/email@domain.com'
        message_id (str): the id of the message to send
    """
    url = "{api_url}/{user_id}/messages/{message_id}/send".format(
        api_url=API_URL,
        user_id=user_id,
        message_id=message_id
        )

    headers = {'Authorization': 'Bearer {}'.format(auth.access_token)}

    req = urllib.request.Request(url, headers=headers, method="POST")
    try:
        urllib.request.urlopen(req)
        logging.getLogger(__name__).info("Message sent")
    except urllib.error.HTTPError as err:
        raise AzureError(err)

