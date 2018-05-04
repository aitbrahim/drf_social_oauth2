from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from permissions import (
    UserObjectOwnerPermission,
    UserPermission
)
from serializers import (
    UserSerializer, AuthenticateSerializer
)

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (UserPermission, UserObjectOwnerPermission)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        hashed_password = make_password(serializer.validated_data['password'])
        serializer.validated_data['password'] = hashed_password
        instance = serializer.save()
        return instance

    def get_object(self):
        pk = self.kwargs.get('pk')
        if pk == 'current':
            return self.request.user

        return super(UserViewSet, self).get_object()

    def update(self, request, *args, **kwargs):
        # Allow partials for updating single values
        kwargs.update(
            dict(
                partial=True
            )
        )
        return super(UserViewSet, self).update(request, *args, **kwargs)


class AuthenticateViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """ Sign In

    Responsible of generating token authentication the end point
    will rely request to apigateway for consumer and return response.

    The sign-in endpoint will get or create consumer from the apigateway
    considering the credentials were validated by service database.
    """
    permission_classes = (permissions.AllowAny,)

    def get_serializer(self, *args, **kwargs):
        return AuthenticateSerializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.generate_token()
        headers = self.get_success_headers(serializer.data)
        # Updates caching when user logs in
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
