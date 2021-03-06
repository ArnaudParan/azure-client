import logging.config
import json

import imports_resolver
from azure_client import get_or_create_credentials, send_email

from settings import LOGGING, get_cred_data

logging.config.dictConfig(LOGGING)

if __name__ == "__main__":
    cred_data = get_cred_data()
    auth = get_or_create_credentials(**cred_data)
    email_id = None
    if email_id is None:
        raise RuntimeError('Please set the value of email_id')
    send_email(auth, "me", email_id)

