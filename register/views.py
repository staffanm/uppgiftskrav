from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from register.models import Uppgift, Krav

def index(request):
    return render(request, "register/index.html")

def kravlist(request):
    return render(request, "register/kravlist.html",
                  {'krav_list':Krav.objects.order_by('kravid')})


def krav(request, kravid):
    k = get_object_or_404(Krav, kravid=kravid)
    return render(request, "register/krav.html", {'krav':k})


def uppgift(request, uppgiftid):
    u = get_object_or_404(Uppgift, uppgiftid=uppgiftid)
    return render(request, "register/uppgift.html", {'uppgift':u})

def uppgiftlist(request):
    return render(request, "register/uppgiftlist.html",
                  {'uppgift_list':Uppgift.objects.order_by('uppgiftid')})
    

    
