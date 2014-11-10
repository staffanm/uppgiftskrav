from django.contrib.auth.models import Group as Myndighet
from django.core import urlresolvers
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from register.models import Uppgift, Krav, Verksamhetsomrade, Bransch, Foretagsform

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

from django import forms

class SearchForm(forms.Form):
#        fields = ['kartlaggande_myndighet',
#                  'kravid',
#                  'namn',
#                  'ursprung',
#                  'leder_till_insamling']
    ANY = [(-1, '---------'),]
    
    kartlaggande_myndighet = forms.ChoiceField(choices=ANY + [(x.id, x.name) for x in Myndighet.objects.all()])
    kravid = forms.CharField(required=False, max_length=Krav._meta.get_field_by_name('kravid')[0].max_length)
    namn = forms.CharField(required=False, max_length=Krav._meta.get_field_by_name('namn')[0].max_length)
    initierande_part = forms.ChoiceField(choices=ANY + Krav.INITIERANDE)
    etjanst = forms.ChoiceField(choices=ANY+Krav.JANEJ)
    ursprung = forms.ChoiceField(choices= ANY + Krav.URSPRUNG)
    leder_till_insamling = forms.ChoiceField(choices= ANY + Krav.JANEJ, initial=Krav.JA)
    avgransat = forms.BooleanField()
    
    
def search(request):
    if request.method == "POST":
        # from pudb import set_trace; set_trace()
        results =  Krav.objects.all()
        kartlaggande_myndighet = request.POST.get('kartlaggande_myndighet', None)
        if kartlaggande_myndighet != '-1':
            results = results.filter(kartlaggande_myndighet__exact=kartlaggande_myndighet)
            
        kravid = request.POST.get('kravid', None)
        if kravid:
            results = results.filter(kravid__icontains=kravid)

        namn = request.POST.get('namn', None)
        if namn:
            results = results.filter(namn__icontains=namn)

        initierande_part = request.POST.get('initierande_part', None)
        if initierande_part != '-1':
            results = results.filter(initierande_part__exact=initierande_part)

        etjanst = request.POST.get('etjanst', None)
        if etjanst != '-1':
            results = results.filter(etjanst__exact=etjanst)

        ursprung = request.POST.get('ursprung', None)
        if ursprung != '-1':
            results = results.filter(ursprung__exact=ursprung)
        
        leder_till_insamling = request.POST.get('leder_till_insamling', None)
        if leder_till_insamling != '-1':
            results = results.filter(leder_till_insamling__exact=leder_till_insamling)

        incompletecount = sum(not x.valid() for x in results)
        if results.count():
            incompletepercentage = int(incompletecount/float(results.count())*100)
        else:
            incompletepercentage = 0
        context = {'resultcount': results.count(),
                   'incompletecount': incompletecount,
                   'incompletepercentage': incompletepercentage,
                   'form': SearchForm(request.POST),
                   'resultset':  results }
    else:
        context = {'form': SearchForm() }
    return render(request, 'register/search.html', context)

class MyListView(ListView):
    paginate_by = 100

class MyDetailView(DetailView):
    pass

class KravList(MyListView):
    model = Krav

class KravDetail(MyDetailView):
    model = Krav
    slug_field = "kravid"
    def get_context_data(self, **kwargs):
        context = super(KravDetail, self).get_context_data(**kwargs)
        try:
            self.object.full_clean()
            context['validation_errors'] = {}
        except ValidationError as e:
            context['validation_errors'] = e.message_dict

        if self.request.user.is_superuser or self.object.kartlaggande_myndighet in self.request.user.groups.all():
            context['adminurl'] = urlresolvers.reverse('admin:register_krav_change', args=(self.object.id,))

        return context

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
