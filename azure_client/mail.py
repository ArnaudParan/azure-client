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

def get_emails(auth, user_id, folder_id='AllItems', **kwargs):
    """
    implementation of that endpoint:
    https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/mail-rest-operations#get-messages

    Args:
        auth (azure_client.authentication.AzureAuth): authentication object with credentials
        user_id (str): the id of the user, either 'me' or 'users/email@domain.com'
        folder_id (str): either the id of the folder or 'Inbox' 'Drafts' 'SentItems' 'DeletedItems'
            by default 'AllItems'
        search (str): to search for specific messages, please see the documentation for syntax ex: "subject:pizza"
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/complex-types-for-mail-contacts-calendar#Search
        filter (str): to filter with some conditions, see in the documentation for syntax ex: "Start/DateTime ge '2016-04-01T08:00'"
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/complex-types-for-mail-contacts-calendar#Filter
        select (str): the elements you want to select separated by a comma ex: 'Sender,Subject,id'
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/complex-types-for-mail-contacts-calendar#Select
        orderby (str): to sort results
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/complex-types-for-mail-contacts-calendar#OrderBy
        top (int): for pagination, the number of entries displayed maximum, 50
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/complex-types-for-mail-contacts-calendar#TopSkip
        skip (int): for pagination, the number of entries to skip
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/complex-types-for-mail-contacts-calendar#TopSkip
        expand (bool): to expand messages and attachments
        count (bool): if true it will return a count of the messages
            https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/complex-types-for-mail-contacts-calendar#Count
    """

    parameters = []
    for key, item in kwargs.items():
        if isinstance(item, bool) and item != False:
            parameters.append("${key}".format(key=key))
        else:
            parameters.append("${key}={item}".format(key=key, item=item))
    url = "{api_url}/{user_id}/MailFolders/{folder_id}/messages?{params}".format(
        api_url=API_URL,
        user_id=user_id,
        folder_id=folder_id,
        params='&'.join(parameters))

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

def delete_email(auth, user_id, message_id):
    """
    implementation of that endpoint:
    https://docs.microsoft.com/en-us/previous-versions/office/office-365-api/api/version-2.0/mail-rest-operations#delete-a-message

    Args:
        auth (azure_client.authentication.AzureAuth): authentication object with credentials
        user_id (str): the id of the user, either 'me' or 'users/email@domain.com'
        message_id (str): the id of the message to send
    """
    url = "{api_url}/{user_id}/messages/{message_id}".format(
        api_url=API_URL,
        user_id=user_id,
        message_id=message_id
        )

    headers = {'Authorization': 'Bearer {}'.format(auth.access_token)}

    req = urllib.request.Request(url, headers=headers, method="DELETE")
    try:
        urllib.request.urlopen(req)
        logging.getLogger(__name__).info("Message deleted")
    except urllib.error.HTTPError as err:
        raise AzureError(err)

def get_all_emails_it(auth, user_id, folder_id='AllItems', pages_limit=None, pages_size=50, **kwargs):
    """
    iterator which goes through all the pages to find all the emails
    """
    i = 0
    args_dict = dict(kwargs, top=pages_size, skip=pages_size * i)
    curr_emails = get_emails(auth, user_id, folder_id, **args_dict)
    while len(curr_emails) != 0:
        yield curr_emails
        if pages_limit is not None and i >= pages_limit:
            break
        i += 1
        args_dict = dict(kwargs, top=pages_size, skip=pages_size * i)
        curr_emails = get_emails(auth, user_id, folder_id, **args_dict)
