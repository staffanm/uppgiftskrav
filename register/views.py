from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from register.models import Uppgift, Krav
from django.contrib.auth.models import Group as Myndighet
def index(request):
    return render(request, "register/index.html")

def kravlist(request):
    return render(request, "register/kravlist.html",
                  {'krav_list':Krav.objects.order_by('kravid'),
                   'mynd_list':Myndighet.objects.annotate(Count('krav')).order_by('-name')
               })

def _get_plot():
    # returns a subplot connected to a figure connected to a canvas
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    fig = Figure()
    ax=fig.add_subplot(1,1,1)
    canvas = FigureCanvas(fig)
    return ax, canvas

def _serve_plot(canvas):
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
    
    
def img_krav_by_myndighet(request):
    # get data
    q = Myndighet.objects.annotate(Count('krav')).order_by('-name')
    labels = [x.name for x in q if x.krav__count]
    sizes = [x.krav__count for x in q if x.krav__count]
    # maxkrav = max([x.krav__count for x in q])
    # explode = [(maxkrav - x.krav__count) / float(maxkrav*10) for x in q if x.krav__count]
    # print(explode)

    # draw data
    ax, canvas = _get_plot()
    ax.pie(sizes, labels=labels, autopct="%d%%", shadow=True)
    ax.axis('equal')

    # serve data
    return _serve_plot(canvas)
        
def img_krav_by_uppgift(request):
    import numpy as np
    q = Uppgift.objects.annotate(Count('krav')).order_by('-uppgiftid')
    names = [x.uppgiftid for x in q]
    values = [x.krav__count for x in q]
    ax, canvas = _get_plot()
    ind = np.arange(q.count())
    ax.bar(ind, values)
    ax.set_xticklabels(names, rotation=270)
    ax.set_xlabel("Uppgift")
    ax.set_ylabel("Antal")
    return _serve_plot(canvas)
    
def krav(request, kravid):
    k = get_object_or_404(Krav, kravid=kravid)
    return render(request, "register/krav.html", {'krav':k})


def uppgift(request, uppgiftid):
    u = get_object_or_404(Uppgift, uppgiftid=uppgiftid)
    return render(request, "register/uppgift.html", {'uppgift':u})

def uppgiftlist(request):
    return render(request, "register/uppgiftlist.html",
                  {'uppgift_list':Uppgift.objects.order_by('uppgiftid')})
    

    
