from base_user import AbstractUser
from django.db import IntegrityError, transaction
from rest_framework.authtoken.models import Token


class User(AbstractUser):

    def make_token(self):
        try:
            with transaction.atomic():
                instance = Token.objects.create(user=self)
        except IntegrityError:
            self.destroy_token()
            instance = Token.objects.create(user=self)
            print 'instance.user.email = {}'.format(instance.user.email)
        return dict(
            key=instance.key
        )

    def destroy_token(self):
        Token.objects.filter(user=self).delete()
