from django.conf.urls import include, url
from django.contrib import admin
from profile import urls as account_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(account_urls, namespace='profile')),
]
