from django.conf.urls import patterns, url

from register import views
from register.models import Krav, Uppgift

from django.views.generic import TemplateView
urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name="index"),
                       url(r'^krav/$', views.KravList.as_view(), name="krav-list"),
                       url(r'^krav/(?P<slug>[A-Z]+\d+)$', views.KravDetail.as_view(), name="krav-detail"),

                       url(r'^uppgift/$', views.UppgiftList.as_view(), name="uppgift-list"),
                       url(r'^uppgift/(?P<slug>[A-Z]+\d+)$', views.UppgiftDetail.as_view(), name="uppgift-detail"),

                       url(r'^form/$', views.ForetagsformList.as_view(), name="form-list"),
                       url(r'^form/(?P<slug>[A-Z]+)$', views.ForetagsformDetail.as_view(), name="form-detail"),

                       url(r'^bransch/$', views.BranschList.as_view(), name="bransch-list"),
                       url(r'^bransch/(?P<slug>[A-Z]+)$', views.BranschDetail.as_view(), name="bransch-detail"),

                       url(r'^myndighet/$', views.MyndighetList.as_view(), name="myndighet-list"),
                       url(r'^myndighet/(?P<pk>\d+)$', views.MyndighetDetail.as_view(), name="myndighet-detail"),

                       url(r'^krav/efter_myndighet.png$', views.img_krav_by_myndighet, name="img_krav_by_myndighet"),
                       url(r'^krav/efter_uppgift.png$', views.img_krav_by_uppgift, name="img_krav_by_uppgift"),
)
