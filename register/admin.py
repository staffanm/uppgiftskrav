# -*- coding: utf-8 -*-
from django.contrib import admin
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

    fieldsets = [
        ('Insamling', {'fields': ['verksamhetsomrade',
                                  'ansvarig_myndighet',
                                  # 'kartlaggande_myndighet',   utgår eftersom UKR i förlängningen ska användas a v alla
                                  'kravid',
                                  'namn',
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
                                  'egna_noteringar'
                              ]}),
        ('När', {'fields': ['kalenderstyrt', # FIXME: om 'nej' ska periodicitet döljas (dynamiskt mha JS?)
                            'periodicitet',
                            'handelsestyrt',
                            'initierande_part',
                            # 'ovrigt_nar'   inaktivera och systematisera bättre i framtiden
                            ]}),
        ('Vem', {'fields': ['bransch',
                            'arbetsgivare',
                            'antal_anstallda',
                            'anstallda',
                            'foretagsform',
                            # 'storlek',
                            # 'storlekskriterier'
                            # 'ovriga_urvalskriterier' # inaktivera i nuvarande kartläggning och systematisera bättre i framtiden
                            # 'antal_foretag' # intressant men har inte sin plats i ett UKR
                            ]}),
        ('Hur', {'fields': ['annan_ingivare',
                            # 'underskrift' # inaktivera i nuvarande kartläggning och systematisera bättre i framtiden
                            'etjanst',
                            'maskintillmaskin',
                            'svarighet_ej_etjanst',
                            'lank_till_blankett',
                            'svarighet_etjanst',
                            'lank_till_etjanst',
                            # 'volymer_tidigare',
                            # 'volymer_2012',
                            # 'volymer_etjanst'  # borttagna utan kommentar
                            'ovrigt_hur']})
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
