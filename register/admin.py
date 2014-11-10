# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db import models
from django.forms import CheckboxSelectMultiple, Textarea, TextInput, RadioSelect

from django.contrib.auth.models import User, Group


from register.models import (Uppgift, Verksamhetsomrade, Bransch,
                             Foretagsform, Krav, Kravomrade, BlankettURL,
                             EtjanstURL)


# We don't use Uppgift anymore -- it's kept around for now, but no
# need to edit it.
# class UppgiftAdmin(admin.ModelAdmin):
#     list_display = ['uppgiftid', 'namn']
# admin.site.register(Uppgift, UppgiftAdmin)


# this new django 1.7 feature removes the need for overriding most
# admin templates
class MyAdminSite(AdminSite):
    site_header = 'Uppgiftskravsregistret'
    site_title = 'Uppgiftskravsregistrets administrationsverktyg'
    index_title = 'Administrera krav mm.'

admin_site = MyAdminSite(name='myadmin')

# this re-enables editing of user and groups under a common
# header. Unfortunately that is not translated (says "Authentication
# and authorization")
admin_site.register(User)
admin_site.register(Group)

class VerksamhetsomradeAdmin(admin.ModelAdmin):
    # only show those kravs that the user may edit (based upon the
    # group/myndighet the krav belongs to, and the group the user
    # belongs to)
    def get_queryset(self, request):
        qs = super(VerksamhetsomradeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(myndighet__in=request.user.groups.all())

admin_site.register(Verksamhetsomrade, VerksamhetsomradeAdmin)


class KravomradeAdmin(admin.ModelAdmin):
    # only show those kravs that the user may edit (based upon the
    # group/myndighet the krav belongs to, and the group the user
    # belongs to)
    def get_queryset(self, request):
        qs = super(KravomradeAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(myndighet__in=request.user.groups.all())

admin_site.register(Kravomrade, KravomradeAdmin)


# Don't know if we ever need to modify this...
class BranschAdmin(admin.ModelAdmin):
    pass

admin_site.register(Bransch, BranschAdmin)


class ForetagsformAdmin(admin.ModelAdmin):
    pass

admin_site.register(Foretagsform, ForetagsformAdmin)


class BlankettInline(admin.TabularInline):
    model = BlankettURL
    extra = 1


class EtjanstInline(admin.TabularInline):
    model = EtjanstURL
    extra = 1


class KravAdmin(admin.ModelAdmin):

    class Media:
        js = ['/static/js/myactions.js']
        
    list_display = ['kravid', 'namn', 'initierande_part', 'avgransad', 'valid']
    # list_editable = ['namn', 'initierande_part', 'avgransad', 'bransch']
    list_filter = ['avgransad', 'kartlaggande_myndighet', 'initierande_part',
                   'etjanst']

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple()},
        models.TextField: {'widget': Textarea(attrs={'cols': 85, 'rows': 3})},
        models.CharField: {'widget': TextInput(attrs={'size': 120})},
        models.URLField: {'widget': TextInput(attrs={'size': 120})},
        # We'd prefer these types to be rendered as groups of radio
        # buttons instead of a select, but doesn't seem to work
        # models.NullBooleanField: {'widget': RadioSelect()},
        # models.BooleanField: {'widget': RadioSelect()},
        # models.IntegerField: {'widget': RadioSelect()}
    }

    fieldsets = [
        ('Uppgiftskrav', {'fields': [
            # 'kravid',
            'namn',
            'verksamhetsomrade',
            'kravomrade',
            'ansvarig_myndighet',
            'kartlaggande_myndighet',
            'lagrum',
            'kortbeskrivning',
            'lank_till_info',
            'leder_till_insamling',
            'galler_from',
            'galler_tom',
            'avgransad',
            'omfattas_av_tjdir',
        ]}),
        ('När aktualiseras uppgiftskravet?', {'fields': [
            'kalenderstyrt',
            'periodicitet',
           'initierande_part',
        ]}),
        ('Vem omfattas av uppgiftskravet?', {'fields': [
            'beror_bransch',
            'bransch',
            'arbetsgivare',
            'beror_foretagsform',
            'foretagsform',
        ]}),
        ('Hur fullgörs uppgiftskravet?', {'fields': [
            'annan_ingivare',
            'blankett',
            'etjanst',
            'maskintillmaskin',
            'ovrigt_hur']}),
        ('Övrigt', {'fields': [
            'egna_noteringar',
            'aktivt']})
    ]
    inlines = [BlankettInline, EtjanstInline]


    # only show those kravs that the user may edit (based upon the
    # group/myndighet the krav belongs to, and the group the user
    # belongs to)
    def get_queryset(self, request):
        qs = super(KravAdmin, self).get_queryset(request)
        if request.user.is_superuser: 
            return qs
        return qs.filter(kartlaggande_myndighet__in=request.user.groups.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "verksamhetsomrade" and not request.user.is_superuser:
            kwargs["queryset"] = Verksamhetsomrade.objects.filter(myndighet__in=request.user.groups.all())
        elif db_field.name == "kravomrade" and not request.user.is_superuser:
            kwargs["queryset"] = Kravomrade.objects.filter(myndighet__in=request.user.groups.all())
        return super(KravAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)        
    
admin_site.register(Krav, KravAdmin)

