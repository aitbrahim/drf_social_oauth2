from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from social_oauth2.exceptions import InvalidEmail, SocialAuthBaseException
from requests.exceptions import HTTPError


class OAuth2Serializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)
    user = None
    key = None

    def validate(self, attrs):
        request = self.context['request']
        try:
            print "access_token = {}".format(attrs['access_token'])
            user = request.backend.do_auth(attrs['access_token'])
            print "user = {}".format(user)
            if user:
                self.user = user
                self.key = request.social_strategy.session.pop('key')
                return {}
            raise serializers.ValidationError(_('We could not log you in'))
        except InvalidEmail as e:
            raise serializers.ValidationError(_('Your email is not valid.'))
        except (SocialAuthBaseException, HTTPError) as e:
            raise serializers.ValidationError(_('We could not log you in'))
