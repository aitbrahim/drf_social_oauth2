import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import force_bytes
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from managers import UserManager


@python_2_unicode_compatible
class AbstractUser(AbstractBaseUser,
                   PermissionsMixin):

    email = models.EmailField(
        _('Email address'),
        null=False,
        blank=False,
        unique=True)

    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    date_joined = models.DateTimeField(
        _('Date joined'),
        auto_now_add=True,
        editable=False)

    last_seen = models.DateTimeField(
        _('Last seen'),
        null=True,
        blank=True,
        editable=False)

    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        editable=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        abstract = True
        ordering = ['-id', ]

    def __str__(self):
        return force_bytes('%s' % self.email)

    def __unicode__(self):
        return u'%s' % self.email
