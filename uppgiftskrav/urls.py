from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^db/', include('register.urls', namespace='register')),
                       url(r'^admin/', include(admin.site.urls))
                       )

