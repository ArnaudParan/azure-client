#!/usr/bin/python3
"""
In that file we have the code which retrieves the data from detrack
website by doing some scraping
"""

import logging
from contextlib import contextmanager
import urllib.request
import urllib.parse
import urllib.error
import json
from selenium.webdriver.support.ui import WebDriverWait
from azure_client.exceptions import AzureError


@contextmanager
def web_driver(driver_generator):
    """
    helps using and closing web drivers wisely,
    the driver generator is a function which takes no argument
    and returns a webdriver
    """
    driver = driver_generator()
    driver.implicitly_wait(10)
    yield driver
    driver.close()


class PageRedirected:  # pylint: disable=too-few-public-methods

    """
    one selenium condition which is triggered when the page url
    corresponds to the one given in argument
    """

    def __init__(self, expected_url):
        self.expected_url = expected_url

    def __call__(self, driver):
        if driver.current_url.split('?', 1)[0] == self.expected_url:
            return driver.current_url
        return False


class AzureAuth:
    """
    Class which allows us to retrieve an access token
    """

    def __init__(self):
        self.scope = ''
        self.client_id = ''
        self.client_secret = ''
        self.access_token = ''
        self.refresh_token = ''
        self.redirect_uri = ''
        self.tenant = ''

    def save_auth(self, filename):
        """
        save the authentification data in one json file
        """
        with open(filename, 'w') as data_file:
            data = {
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': self.scope,
                'tenant': self.tenant,
                'redirect_uri': self.redirect_uri
                }
            json.dump(data, data_file)

    def get_auth_from_file(self, filename):
        """
        get the authentification from a json file
        """
        with open(filename, 'r') as data_file:
            data = json.load(data_file)
            self.access_token = data.get('access_token', '')
            self.refresh_token = data.get('refresh_token', '')
            self.client_id = data.get('client_id', '')
            self.client_secret = data.get('client_secret', '')
            self.scope = data.get('scope', '')
            self.tenant = data.get('tenant', '')
            self.redirect_uri = data.get('redirect_uri', '')

    def authenticate(self, driver_generator, client_id, client_secret, scope, tenant, redirect_uri):  # pylint: disable=too-many-arguments
        """
        goes through the oauth authentication flow
        takes the client id, client secret, the scopes formatted as string or list,
        the tenant which sould be an identifier or common or organization, and
        the redirect_uri that you used for the application
        """
        logging.getLogger(__name__).info('Authenticating the user')
        if isinstance(scope, list):
            for item in scope:
                if not isinstance(item, str):
                    raise ValueError('Unexpected scope')
            scope = ' '.join(scope)
        elif not isinstance(scope, str):
            raise ValueError('Unexpected scope')

        self.client_id = client_id
        self.scope = scope
        self.tenant = tenant
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret

        code = AzureAuth._get_authorization_code(
            driver_generator,
            self.client_id,
            self.scope,
            self.tenant,
            self.redirect_uri)
        self.access_token, self.refresh_token = AzureAuth._get_token(
            self.client_id,
            self.client_secret,
            code, self.tenant,
            self.redirect_uri)

    def refresh_access_token(self):
        """
        that function allows to retrieve a new access token using a
        refresh token
        """
        logging.getLogger(__name__).info('Refreshing the token')
        self.access_token, self.refresh_token = AzureAuth._get_access_token_from_refresh_token(
            self.client_id,
            self.client_secret,
            self.refresh_token,
            self.tenant,
            self.redirect_uri)

    @staticmethod
    def _get_authorization_code(driver_generator, client_id, scope, tenant, redirect_uri):
        """
        gets the authorization code to start the oauth process
        """
        authorize_url = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize".format(tenant=tenant)  # pylint: disable=line-too-long

        code = None

        with web_driver(driver_generator) as driver:
            driver.get('{url}?client_id={client_id}&scope={scope}&response_type=code&redirect_uri={redirect_uri}'.format(  # pylint: disable=line-too-long
                url=authorize_url,
                client_id=client_id,
                scope=scope,
                redirect_uri=redirect_uri))

            wait = WebDriverWait(driver, 120)
            url = wait.until(PageRedirected(redirect_uri))
            code = urllib.parse.parse_qs(url.split('?', 1)[1])['code'][0]

        return code

    @staticmethod
    def _get_token(client_id, client_secret, code, tenant, redirect_uri):
        """
        gets access token from authentification code
        """
        token_url = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token".format(tenant=tenant)  # pylint: disable=line-too-long
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code"
            }
        params = urllib.parse.urlencode(data).encode("utf8")
        req = urllib.request.Request(token_url, data=params)
        resp = urllib.request.urlopen(req)
        resp_data = json.load(resp)
        access_token = resp_data['access_token']
        refresh_token = resp_data.get('refresh_token', '')

        return access_token, refresh_token

    @staticmethod
    def _get_access_token_from_refresh_token(\
            client_id,
            client_secret,
            refresh_token,
            tenant,
            redirect_uri):
        """
        refresh an access token using a refresh token
        """
        token_url = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token".format(tenant=tenant)  # pylint: disable=line-too-long
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "redirect_uri": redirect_uri,
            "grant_type": "refresh_token"
            }
        params = urllib.parse.urlencode(data).encode("utf8")
        req = urllib.request.Request(token_url, data=params)
        try:
            resp = urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            raise AzureError(err)
        resp_data = json.load(resp)
        access_token = resp_data['access_token']
        refresh_token = resp_data['refresh_token']

        return access_token, refresh_token
