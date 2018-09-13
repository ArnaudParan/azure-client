import logging.config
import json

import imports_resolver
from azure_client import get_or_create_credentials, send_email

from settings import LOGGING

logging.config.dictConfig(LOGGING)

if __name__ == "__main__":
    try:
        with open('examples/azure_ids.json', 'r') as f:
            cred_data = json.load(f)
    except FileNotFoundError as err:
        logging.getLogger(__name__).error("Please create an azure_ids.json before trying this example")
        raise err
    auth = get_or_create_credentials(**cred_data)
    email_id = None
    if email_id is None:
        raise RuntimeError('Please set the value of email_id')
    send_email(auth, "me", email_id)

