import logging


import logging

from requests import HTTPError
from rest_framework import serializers
from .serializers import OAuth2RequiredFieldsSerializer


logger = logging.getLogger(__name__)


def validate_data(strategy, details, backend, user=None, *args, **kwargs):
    if not user:
        serializer = OAuth2RequiredFieldsSerializer(data=details, context={'request': strategy.request})
        if not serializer.is_valid(raise_exception=False):
            try:
                backend.revoke_token(kwargs['response']['access_token'], kwargs['uid'])
            except HTTPError:
                logger.error('Could not revoke the access token for {}'.format(backend.name),
                             extra={
                                 'user_info': details,
                                 'backend': backend.name
                             })
            raise serializers.ValidationError(serializer.errors)


def create_token(strategy, user, is_new, *args, **kwargs):
    request = strategy.request
    print "strategy = {}".format(strategy)
    print "request = {}".format(request)
    strategy.session['key'] = user.make_token()['key']
    strategy.session['is_new'] = is_new
