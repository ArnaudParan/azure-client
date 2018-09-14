import logging.config
import json

import imports_resolver
from azure_client import get_or_create_credentials, get_emails

from settings import LOGGING, get_cred_data

logging.config.dictConfig(LOGGING)

if __name__ == "__main__":
    cred_data = get_cred_data()
    auth = get_or_create_credentials(**cred_data)
    emails = get_emails(auth, "me", "Drafts", select="id")
    print('Number of emails: {}'.format(len(emails)))
    print(emails)
