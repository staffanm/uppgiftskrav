from django.conf.urls import patterns, url

from register import views

urlpatterns = patterns('',
                       url(r'^uppgift/$', views.uppgifter),
                       url(r'^krav/$', views.kravlist),
                       url(r'^krav/(?P<krav_id>\d+)$', views.krav),
                       url(r'^$', views.index),
)
