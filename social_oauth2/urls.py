from django.conf.urls import url, include
from .views import OAuth2View, home


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^users/auth/(?P<backend>[^/]+)', OAuth2View.as_view(),
        name='register_by_access_token'),
]
