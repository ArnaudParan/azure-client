"""
The exceptions of the package
"""

import logging
import json


class AzureError(Exception):

    """
    class which handles the azure web errors
    """

    def __init__(self, http_error):
        super().__init__()
        self.code = http_error.code
        self.reason = http_error.reason
        res = http_error.read()
        self.error_data = {}
        logging.getLogger(__name__).debug("Azure web error\n\n%s", res)
        try:
            self.error_data = json.loads(res)
            if isinstance(self.error_data['error'], str):
                self.error = self.error_data['error']
                self.error_description = self.error_data['error_description']
            elif isinstance(self.error_data['error'], dict):
                self.error = self.error_data['error']['code']
                self.error_description = self.error_data['error']['message']
        except json.decoder.JSONDecodeError:
            self.error = ''
            self.error_description = res

    def __str__(self):
        return 'Azure Error {}:\n\n{}\n\n{}'.format(self.code, self.error, self.error_description)
