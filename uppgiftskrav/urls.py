from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.views.generic import RedirectView

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', RedirectView.as_view(url="/db/")),
                       url(r'^db/', include('register.urls', namespace='register')),
                       url(r'^admin/', include(admin.site.urls))
                       )

