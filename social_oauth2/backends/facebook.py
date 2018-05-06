"""
Facebook OAuth2 and Canvas Application backends, docs at:
    https://python-social-auth.readthedocs.io/en/latest/backends/facebook.html
"""
import hmac
import time
import json
import base64
import hashlib

# from .oauth import BaseOAuth2
from ..exceptions import AuthException, AuthCanceled, AuthUnknownError, \
                         AuthMissingParameter


API_VERSION = 3.0
from .base import BaseAuth


class FacebookOAuth2(BaseAuth):
    """Facebook OAuth2 authentication backend"""
    name = 'facebook'
    USER_DATA_URL = 'https://graph.facebook.com/v{version}/me'

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        params = self.setting('PROFILE_EXTRA_PARAMS', {})
        params['access_token'] = access_token
        if self.setting('APPSECRET_PROOF', True):
            _, secret = self.get_key_and_secret()
            params['appsecret_proof'] = hmac.new(
                secret.encode('utf8'),
                msg=access_token.encode('utf8'),
                digestmod=hashlib.sha256
            ).hexdigest()

        version = self.setting('API_VERSION', API_VERSION)
        return self.get_json(self.USER_DATA_URL.format(version=version),
                             params=params)

    def do_auth(self, access_token, response=None, *args, **kwargs):

        response = response or {}

        data = self.user_data(access_token)

        if not isinstance(data, dict):
            raise AuthUnknownError(self, 'An error ocurred while retrieving '
                                         'users Facebook data')

        data['access_token'] = access_token
        if 'expires_in' in response:
            data['expires'] = response['expires_in']

        if self.data.get('granted_scopes'):
            data['granted_scopes'] = self.data['granted_scopes'].split(',')

        if self.data.get('denied_scopes'):
            data['denied_scopes'] = self.data['denied_scopes'].split(',')

        kwargs.update({'backend': self, 'response': data})
        return self.strategy.authenticate(*args, **kwargs)

    def get_user_details(self, response):
        """Return user details from Facebook account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('name', ''),
            response.get('first_name', ''),
            response.get('last_name', '')
        )
        return {'username': response.get('username', response.get('name')),
                'email': response.get('email', ''),
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}
