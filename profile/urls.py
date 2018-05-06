from django.conf.urls import url, include
from rest_framework import routers

from . import views
from .views import OAuth2View
router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
from profile.views import  home

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^sign-in/$',
        views.AuthenticateViewSet.as_view({'post': 'create'}),
        name='sign-in'),

    url(r'^users/auth', OAuth2View.as_view(),
        name='register_by_access_token'),
]

urlpatterns += router.urls
