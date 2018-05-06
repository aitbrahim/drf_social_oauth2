"""Django ORM models for Social Auth"""
from django.db import models
from django.conf import settings
from .storage import DjangoUserMixin, BaseDjangoStorage


from django.db.utils import IntegrityError
from .utils import setting_name
#
from .utils import get_rel_model


from .fields import JSONField
from .managers import UserSocialAuthManager


USER_MODEL = getattr(settings, setting_name('USER_MODEL'), None) or \
             getattr(settings, 'AUTH_USER_MODEL', None) or \
             'auth.User'
UID_LENGTH = getattr(settings, setting_name('UID_LENGTH'), 255)
EMAIL_LENGTH = getattr(settings, setting_name('EMAIL_LENGTH'), 254)
NONCE_SERVER_URL_LENGTH = getattr(
    settings, setting_name('NONCE_SERVER_URL_LENGTH'), 255)
ASSOCIATION_SERVER_URL_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_SERVER_URL_LENGTH'), 255)
ASSOCIATION_HANDLE_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_HANDLE_LENGTH'), 255)


class AbstractUserSocialAuth(models.Model, DjangoUserMixin):
    """Abstract Social Auth association model"""
    user = models.ForeignKey(USER_MODEL, related_name='social_auth',
                             on_delete=models.CASCADE)
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    extra_data = JSONField()
    objects = UserSocialAuthManager()

    def __str__(self):
        return str(self.user)

    class Meta:
        abstract = True

    @classmethod
    def get_social_auth(cls, provider, uid):
        try:
            return cls.objects.select_related('user').get(provider=provider,
                                                          uid=uid)
        except cls.DoesNotExist:
            return None

    @classmethod
    def username_max_length(cls):
        username_field = cls.username_field()
        field = cls.user_model()._meta.get_field(username_field)
        return field.max_length

    @classmethod
    def user_model(cls):
        user_model = get_rel_model(field=cls._meta.get_field('user'))
        return user_model


class UserSocialAuth(AbstractUserSocialAuth):
    """Social Auth association model"""

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        db_table = 'social_auth_usersocialauth'


class DjangoStorage(BaseDjangoStorage):
    user = UserSocialAuth

    @classmethod
    def is_integrity_error(cls, exception):
        return exception.__class__ is IntegrityError
