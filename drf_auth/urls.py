from django.conf.urls import url, include
from rest_framework import routers
from . import views
router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^sign-in/$',
        views.AuthenticateViewSet.as_view({'post': 'create'}),
        name='sign-in'),
]

urlpatterns += router.urls
