from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the front page")

def kravlist(request):
    return HttpResponse("Hello, world. You're looking at all krav")

def krav(request, krav_id):
    return HttpResponse("This is krav %s" % krav_id)


from register.models import Uppgift
def uppgifter(request):
    
    return HttpResponse("Hello, world. You're looking at " + ', '.join([str(u) for u in Uppgift.objects.order_by('namn')]))

    
