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

