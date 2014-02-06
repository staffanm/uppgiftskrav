from django.shortcuts import render

from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.models import Group as Myndighet


from register.models import Uppgift, Krav, Verksamhetsomrade, Bransch, Foretagsform

def index(request):
    return render(request, "register/index.html")


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
    q = Myndighet.objects.annotate(Count('ansvarig_for')).order_by('-name')
    labels = [x.name for x in q if x.ansvarig_for__count]
    sizes = [x.ansvarig_for__count for x in q if x.ansvarig_for__count]
    # maxansvarig_for = max([x.ansvarig_for__count for x in q])
    # explode = [(maxansvarig_for - x.ansvarig_for__count) / float(maxansvarig_for*10) for x in q if x.ansvarig_for__count]
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


class MyListView(ListView):
    paginate_by = 100

class MyDetailView(DetailView):
    pass

class KravList(MyListView):
    model = Krav

class KravDetail(MyDetailView):
    model = Krav
    slug_field = "kravid"

class UppgiftList(MyListView):
    model = Uppgift

class UppgiftDetail(MyDetailView):
    model = Uppgift
    slug_field = "uppgiftid"

class BranschList(MyListView):
    model = Bransch

class BranschDetail(MyDetailView):
    model = Bransch
    slug_field = "snikod"

class ForetagsformList(MyListView):
    model = Foretagsform

class ForetagsformDetail(MyDetailView):
    model = Foretagsform
    slug_field = "formkod"

class VerksamhetsomradeList(MyListView):
    model = Verksamhetsomrade

class VerksamhetsomradeDetail(MyDetailView):
    model = Verksamhetsomrade

class MyndighetList(MyListView):
    model = Myndighet
    template_name = "register/myndighet_list.html" # override default auth/group_list.html

class MyndighetDetail(MyDetailView):
    model = Myndighet
    template_name = "register/myndighet_detail.html" # override default auth/group_detail.html

class IndexView(TemplateView):
    template_name = "register/index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'krav_cnt': Krav.objects.count(),
                        'uppgift_cnt': Uppgift.objects.count(),
                        'myndighet_cnt': Myndighet.objects.count()})
        return context    
