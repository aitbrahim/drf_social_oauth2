from django.contrib.auth import authenticate, get_user_model
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    password = serializers.CharField(label=_('Password'), write_only=True, validators=[
        validators.MinLengthValidator(8, _('Ensure password has at least 8 characters.')),
        validators.MaxLengthValidator(25, _('Ensure password has no more than 25 characters.'))
    ])
    email = serializers.EmailField(label='Email address', max_length=254, validators=[
        UniqueValidator(queryset=get_user_model().objects.all(),
                        message=_('user with this Email address already exists.'))
    ])

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def validate(self, data):

        # Never allow updating password on UserSerializer
        if hasattr(self.instance, 'id'):
            if 'password' in data:
                raise serializers.ValidationError(_('Cannot update password'))
            if 'email' in data:
                raise serializers.ValidationError(_('Cannot update email'))
        return data


class AuthenticateSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(label=_('Password'), write_only=True)
    key = serializers.CharField(label=_('Key'), read_only=True)
    email = serializers.CharField(label=_('Email'))

    def generate_token(self):
        validated_data = self.validated_data
        user = validated_data['user']
        token = user.make_token()
        print token
        self.validated_data.update(
            token
        )

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        if not all([email, password]):
            # Update below message with
            # Must include "username" and "password".
            # Require updating translations too
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        user = authenticate(email=email, password=password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        attrs['id'] = user.id
        return attrs


from social_core.exceptions import InvalidEmail, SocialAuthBaseException
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


class OAuth2RequiredFieldsSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError(_('A user already exists with this email.'))
        request = self.context['request']
        if request:
            request.session['verify_email'] = True

        return value
