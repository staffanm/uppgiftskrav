# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple, Textarea

from register.models import Uppgift, Verksamhetsomrade, Bransch, Foretagsform, Krav
# Register your models here.
class UppgiftAdmin(admin.ModelAdmin):
    list_display = ['uppgiftid', 'namn']

admin.site.register(Uppgift, UppgiftAdmin)


class VerksamhetsomradeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Verksamhetsomrade, VerksamhetsomradeAdmin)

class BranschAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bransch, BranschAdmin)

class ForetagsformAdmin(admin.ModelAdmin):
    pass

admin.site.register(Foretagsform, ForetagsformAdmin)


class KravAdmin(admin.ModelAdmin):
    list_display = ['kravid', 'namn', 'valid']
    list_filter = ['kartlaggande_myndighet', 'initierande_part', 'etjanst', 'leder_till_insamling']
    formfield_overrides = { models.ManyToManyField: {'widget': CheckboxSelectMultiple()},
                            models.TextField: {'widget': Textarea(attrs={'cols':80, 'rows':3})}}

    fieldsets = [
        ('Uppgiftskrav', {'fields':[ 'namn',
                                     'verksamhetsomrade',
                                  'ansvarig_myndighet',
                                  'kartlaggande_myndighet',   # utgår på sikt eftersom UKR i förlängningen ska användas a v alla
                                  # 'forfattning', # förifyllt från Malin, anges
                                  # 'paragraf',    # istället i lagrum/Författningsstöd
                                  'lagrum',
                                  # 'ursprung',    # utgår
                                  # 'beskrivning', # utgår
                                  # 'anteckning',  # utgår
                                  'kortbeskrivning',
                                  'lank_till_info',
                                  'leder_till_insamling',
                                  'galler_from',
                                  'galler_tom',
                              ]}),
        ('När aktualiseras uppgiftkravet?', {'fields': ['kalenderstyrt', # FIXME: om 'nej' ska periodicitet döljas (dynamiskt mha JS?)
                            'periodicitet',
                            'handelsestyrt',
                            'initierande_part',
                            # 'ovrigt_nar'   inaktivera och systematisera bättre i framtiden
                            ]}),
        ('Vilka företag omfattas av uppgiftskravet?', {'fields': ['bransch',
                            'arbetsgivare',
                            # 'antal_anstallda',
                            # 'anstallda',  # oklart nyttan?
                            'foretagsform',
                            # 'storlek',
                            # 'storlekskriterier'
                            # 'ovriga_urvalskriterier' # inaktivera i nuvarande kartläggning och systematisera bättre i framtiden
                            # 'antal_foretag' # intressant men har inte sin plats i ett UKR
                            ]}),
        ('Hur fullgörs uppgiftskravet?', {'fields': ['annan_ingivare',
                            # 'underskrift' # inaktivera i nuvarande kartläggning och systematisera bättre i framtiden
                            'blankett',                                                     
                            'lank_till_blankett',
                            'etjanst',
                            'lank_till_etjanst',
                            'maskintillmaskin',
                            # 'svarighet_ej_etjanst',
                            # 'svarighet_etjanst',
                            # 'volymer_tidigare',
                            # 'volymer_2012',
                            # 'volymer_etjanst'  # borttagna utan kommentar
                            'ovrigt_hur']}),
        ('Övrigt', {'fields': ['egna_noteringar',
                               'aktivt']})
    ]
    
    # only show those kravs that the user may edit (based upon the
    # group/myndighet the krav belongs to, and the group the user
    # belongs to)
    def get_queryset(self, request):
        qs = super(KravAdmin, self).get_queryset(request)
        if request.user.is_superuser: 
            return qs
        return qs.filter(kartlaggande_myndighet__in=request.user.groups.all())



admin.site.register(Krav, KravAdmin)
