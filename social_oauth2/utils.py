from functools import wraps
from django.conf import settings
from .exceptions import MissingBackend
from django.urls import reverse
from importlib import import_module

import re
import unicodedata
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
# import social_core

import six
import django
from django.db import models


# ---------------------------check------------------------------
SETTING_PREFIX = 'SOCIAL_AUTH'

def to_setting_name(*names):
    return '_'.join([name.upper().replace('-', '_') for name in names if name])


def setting_name(*names):
    return to_setting_name(*((SETTING_PREFIX,) + names))
# ---------------------------------------------------------------

PARTIAL_TOKEN_SESSION_NAME = 'partial_pipeline_token'


def module_member(name):
    mod, member = name.rsplit('.', 1)
    module = import_module(mod)
    return getattr(module, member)


AUTHENTICATION_BACKENDS = settings.AUTHENTICATION_BACKENDS
STRATEGY = getattr(settings, 'STRATEGY', 'social_oauth2.strategy.DjangoStrategy')
STORAGE = getattr(settings, 'STORAGE', 'social_oauth2.models.DjangoStorage')


def load_strategy():
    return module_member(STRATEGY)(module_member(STORAGE))


def load_backend(strategy, name, redirect_uri):
    BACKENDS = {}
    for backend in AUTHENTICATION_BACKENDS:
        BACKEND = module_member(backend)
        BACKENDS[BACKEND.name] = BACKEND
    print "BACKENDS[name] = {}".format(BACKENDS[name])
    Backend = BACKENDS[name]

    return Backend(strategy, redirect_uri)


def psa(redirect_uri=None):
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            backend = self.kwargs.get('backend', None)
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = reverse(redirect_uri, args=(backend,))
            request.social_strategy = load_strategy()
            try:
                request.backend = None
                request.backend = load_backend(request.social_strategy, backend, uri)
                print "request = {}".format(request)
                print "request.backend = {}".format(request.backend)

            except MissingBackend:
                raise Exception('Backend not found')
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator

class SSLHttpAdapter(HTTPAdapter):
    """"
    Transport adapter that allows to use any SSL protocol. Based on:
    http://requests.rtfd.org/latest/user/advanced/#example-specific-ssl-version
    """
    def __init__(self, ssl_protocol):
        self.ssl_protocol = ssl_protocol
        super(SSLHttpAdapter, self).__init__()

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=self.ssl_protocol
        )

    @classmethod
    def ssl_adapter_session(cls, ssl_protocol):
        session = requests.Session()
        session.mount('https://', SSLHttpAdapter(ssl_protocol))
        return session


def user_agent():
    """Builds a simple User-Agent string to send in requests"""
    return 'social-auth-2'


# This slugify version was borrowed from django revision a61dbd6
def slugify(value):
    """Converts to lowercase, removes non-word characters (alphanumerics
    and underscores) and converts spaces to hyphens. Also strips leading
    and trailing whitespace."""
    value = unicodedata.normalize('NFKD', six.text_type(value)) \
                       .encode('ascii', 'ignore') \
                       .decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value)


def get_rel_model(field):
    if django.VERSION >= (2, 0):
        return field.remote_field.model

    user_model = field.rel.to
    if isinstance(user_model, six.string_types):
        app_label, model_name = user_model.split('.')
        user_model = models.get_model(app_label, model_name)
    return user_model
