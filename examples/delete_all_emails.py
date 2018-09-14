import logging.config
import json

import imports_resolver
from azure_client import get_or_create_credentials, get_all_emails_it, delete_email

from settings import LOGGING, get_cred_data

logging.config.dictConfig(LOGGING)

if __name__ == "__main__":
    folder = "Drafts"
    execute = input('This program will delete all your messages in {}, are you sure you want to do that (y|n) :'.format(folder))
    if execute not in ('y', 'Y'):
        exit()
    cred_data = get_cred_data()
    auth = get_or_create_credentials(**cred_data)
    for emails_data in get_all_emails_it(auth, "me", folder, select="id"):
        for d in emails_data:
            delete_email(auth, "me", d['id'])
