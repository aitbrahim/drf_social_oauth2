from rest_framework import permissions


class UserObjectOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserPermission(permissions.BasePermission):
    """
    Allowed Mthods:
        Anonymous Users:
            - POST
        Authenticated Users:
            - PATCH
            - GET
            - DELETE
            - HEAD
            - OPTIONS
    """
    def has_permission(self, request, view):
        methods_allowed_for_anonymous = ('POST', )
        methods_allowed_for_authenticated = ('GET', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS')
        if request.method in methods_allowed_for_anonymous and request.user.is_anonymous:
            return True
        print 'request.user.is_authenticated = {}'.format(request.user.is_authenticated)
        if request.method in methods_allowed_for_authenticated and request.user.is_authenticated:
            return True

        return False
