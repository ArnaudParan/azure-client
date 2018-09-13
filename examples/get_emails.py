import logging.config
import json

import imports_resolver
from azure_client import get_or_create_credentials, get_emails

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
    print(get_emails(auth, "me", "Drafts", ["id"]))
