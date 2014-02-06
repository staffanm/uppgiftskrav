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
    list_display = ['kravid', 'namn']
    list_filter = ['kartlaggande_myndighet', 'leder_till_insamling']

    # only show those kravs that the user may edit (based upon the
    # group/myndighet the krav belongs to, and the group the user
    # belongs to)
    def get_queryset(self, request):
        qs = super(KravAdmin, self).get_queryset(request)
        if request.user.is_superuser: 
            return qs
        return qs.filter(myndighet__in=request.user.groups.all())

admin.site.register(Krav, KravAdmin)
