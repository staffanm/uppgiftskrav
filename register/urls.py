from django.conf.urls import patterns, url

from register import views

urlpatterns = patterns('',
                       url(r'^uppgift/$', views.uppgiftlist, name="uppgiftlist"),
                       url(r'^uppgift/(?P<uppgiftid>[A-Z]+\d+)$', views.uppgift, name="uppgift"),
                       url(r'^krav/$', views.kravlist, name="kravlist"),
                       url(r'^krav/(?P<kravid>[A-Z]+\d+)$', views.krav, name="krav"),
                       url(r'^$', views.index),
)
