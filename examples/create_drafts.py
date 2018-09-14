"""
basic example which creates email drafts
"""

import json
import base64
import logging.config
import os
from pathlib import Path
from selenium import webdriver

import imports_resolver
from azure_client import create_draft, get_or_create_credentials

from settings import LOGGING, get_cred_data


if __name__ == "__main__":
    logging.config.dictConfig(LOGGING)
    cred_data = get_cred_data()
    auth = get_or_create_credentials(**cred_data)

    with open('examples/test_email.json', 'r') as f:
        email_data = json.load(f)

    for _ in range(100):
        create_draft(auth, **email_data)

    EMAIL_ID = create_draft(auth, **email_data)

    NAME = "attachment.tsv"
    with open('examples/data/attachment.tsv', 'rb') as f:
        CONTENT_BYTES = base64.b64encode(f.read()).decode('utf8')
        create_draft(auth, **email_data, attachments_list=[{"Name": NAME, "ContentBytes": CONTENT_BYTES, "@odata.type": "#Microsoft.OutlookServices.FileAttachment"}])
