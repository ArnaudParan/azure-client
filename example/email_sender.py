"""
basic example which creates email drafts
"""

import base64
import logging.config
import os
from pathlib import Path
from selenium import webdriver
from azure_client import create_draft, get_or_create_credentials


LOGGING = {
    'version': 1,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)s:%(lineno)d %(levelname)-8s %(processName)-10s %(message)s'
            }
        },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'level': 'DEBUG'
            },
        },
    'loggers': {
        'azure_client': {
            'level': 'DEBUG',
            'handlers': ['console']
            },
        '__main__': {
            'level': 'DEBUG',
            'handlers': ['console']
            }
        },
    }

logging.config.dictConfig(LOGGING)


PRIVATE_KEY = 'private-key-here'  # TODO
CLIENT_ID = 'client-id-here'  # TODO
SCOPE = ["offline_access", "mail.readwrite"]
TENANT = "tenant-here"  # TODO
REDIRECT_URI = "http://localhost/"
FILENAME = "example_auth.json"

AUTH = get_or_create_credentials(CLIENT_ID, PRIVATE_KEY, SCOPE, TENANT, REDIRECT_URI, FILENAME)

SUBJECT = 'test outlook rest api'
BODY = 'This is a <p>Test</p>.'
ADDRESSES = ['test@domain.com']
USER_ID = 'me'

EMAIL_ID = create_draft(AUTH, SUBJECT, BODY, ADDRESSES, USER_ID)

NAME = "attachment.tsv"
with open('example/data/attachment.tsv', 'rb') as f:
    CONTENT_BYTES = base64.b64encode(f.read()).decode('utf8')
    create_draft(AUTH, SUBJECT, BODY, ADDRESSES, USER_ID, [{"Name": NAME, "ContentBytes": CONTENT_BYTES, "@odata.type": "#Microsoft.OutlookServices.FileAttachment"}])
