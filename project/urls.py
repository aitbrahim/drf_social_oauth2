from django.conf.urls import include, url
from django.contrib import admin
from profile import urls as account_urls
from social_oauth2 import urls as social_oauth2_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(account_urls, namespace='profile')),
    url(r'^', include(social_oauth2_urls, namespace='social_oauth2')),
]
