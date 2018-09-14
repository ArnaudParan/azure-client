import json
import warnings


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

def get_cred_data():
    try:
        with open('examples/azure_ids.json', 'r') as f:
            cred_data = json.load(f)
    except FileNotFoundError as err:
        warnings.warn("Please create an azure_ids.json before trying this example", UserWarning)
        raise err
    return cred_data
