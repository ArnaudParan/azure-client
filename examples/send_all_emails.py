import logging.config
import json

import imports_resolver
from azure_client import get_or_create_credentials, get_all_emails_it, send_email

from settings import LOGGING, get_cred_data

logging.config.dictConfig(LOGGING)

if __name__ == "__main__":
    cred_data = get_cred_data()
    auth = get_or_create_credentials(**cred_data)
    emails_data = get_emails(auth, "me", "Drafts", select="id")

    for emails_data in get_all_emails_it(auth, "me", folder, select="id"):
        for d in emails_data:
        send_email(auth, "me", d['id'])
