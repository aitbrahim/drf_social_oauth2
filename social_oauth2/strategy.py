from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect, resolve_url
from django.utils.encoding import force_text
from django.utils.functional import Promise
from .utils import setting_name
from .pipeline import DEFAULT_AUTH_PIPELINE


class BaseStrategy(object):

    def __init__(self, storage=None):
        self.storage = storage

    def setting(self, name, default=None, backend=None):
        names = [setting_name(name), name]
        if backend:
            names.insert(0, setting_name(backend.name, name))
        for name in names:
            try:
                return self.get_setting(name)
            except (AttributeError, KeyError):
                pass
        return default

    def create_user(self, *args, **kwargs):
        return self.storage.user.create_user(*args, **kwargs)

    def get_user(self, *args, **kwargs):
        return self.storage.user.get_user(*args, **kwargs)

    def get_pipeline(self, backend=None):
        return self.setting('PIPELINE', DEFAULT_AUTH_PIPELINE, backend)

    def get_backends(self):
        """Return configured backends"""
        return self.setting('AUTHENTICATION_BACKENDS', [])

    def absolute_uri(self, path=None):
        uri = self.build_absolute_uri(path)
        if uri and self.setting('REDIRECT_IS_HTTPS'):
            uri = uri.replace('http://', 'https://')
        return uri

    def request_data(self, merge=True):
        """Return current request data (POST or GET)"""
        raise NotImplementedError('Implement in subclass')

    def build_absolute_uri(self, path=None):
        """Build absolute URI with given (optional) path"""
        raise NotImplementedError('Implement in subclass')

    def get_setting(self, name):
        """Return value for given setting name"""
        raise NotImplementedError('Implement in subclass')





class DjangoStrategy(BaseStrategy):

    def __init__(self, storage, request=None):
        self.request = request
        self.session = request.session if request else {}
        super(DjangoStrategy, self).__init__(storage)

    def authenticate(self, backend, *args, **kwargs):
        """Trigger the authentication mechanism tied to the current
        framework"""
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = backend
        args, kwargs = self.clean_authenticate_args(*args, **kwargs)
        return backend.authenticate(*args, **kwargs)

    def clean_authenticate_args(self, *args, **kwargs):
        """Cleanup request argument if present, which is passed to
        authenticate as for Django 1.11"""
        if len(args) > 0 and isinstance(args[0], HttpRequest):
            kwargs['request'], args = args[0], args[1:]
        return args, kwargs

    def request_data(self, merge=True):
        if not self.request:
            return {}
        if merge:
            data = self.request.GET.copy()
            data.update(self.request.POST)
        elif self.request.method == 'POST':
            data = self.request.POST
        else:
            data = self.request.GET
        return data

    def build_absolute_uri(self, path=None):
        if self.request:
            return self.request.build_absolute_uri(path)
        else:
            return path

    def get_setting(self, name):
        value = getattr(settings, name)
        # Force text on URL named settings that are instance of Promise
        if name.endswith('_URL'):
            if isinstance(value, Promise):
                value = force_text(value)
            value = resolve_url(value)
        return value
