from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    #url(r'^plus/', include('plus.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', admin.site.urls),
    url(r'^$','plus.views.index'),
    url(r'^oauth2callback', 'plus.views.auth_return')
]

''''
import os
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.conf.urls import patterns, include
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'plus.views.index'),
    (r'^oauth2callback', 'plus.views.auth_return'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)'''