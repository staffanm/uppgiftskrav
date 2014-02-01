from django.conf.urls import patterns, url

from register import views

urlpatterns = patterns('',
                       url(r'^uppgift/$', views.uppgiftlist, name="uppgiftlist"),
                       url(r'^uppgift/(?P<uppgiftid>[A-Z]+\d+)$', views.uppgift, name="uppgift"),
                       url(r'^krav/efter_myndighet.png$', views.img_krav_by_myndighet, name="img_krav_by_myndighet"),
                       url(r'^krav/efter_uppgift.png$', views.img_krav_by_uppgift, name="img_krav_by_uppgift"),
                       url(r'^krav/$', views.kravlist, name="kravlist"),
                       url(r'^krav/(?P<kravid>[A-Z]+\d+)$', views.krav, name="krav"),
                       url(r'^$', views.index),
)
