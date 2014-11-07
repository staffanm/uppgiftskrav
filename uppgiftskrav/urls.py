from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic import RedirectView

from register.admin import admin_site

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', RedirectView.as_view(url="/db/")),
                       url(r'^db/', include('register.urls', namespace='register')),
                       url(r'^admin/', include(admin_site.urls)),
                       # url(r'^admin/', include("massadmin.urls"))
                       )

