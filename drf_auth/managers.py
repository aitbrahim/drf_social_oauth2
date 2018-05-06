from django.contrib.auth.models import BaseUserManager, Group
from django.db.models import Manager


class UserManager(BaseUserManager, Manager):

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(
            email=UserManager.normalize_email(email),
            password=password,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(
            email=UserManager.normalize_email(email),
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )
        user.save(using=self._db)
        return user
