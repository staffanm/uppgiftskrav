from django.contrib import admin
from register.models import Uppgift, Krav
# Register your models here.
class UppgiftAdmin(admin.ModelAdmin):
    list_display = ['uppgiftid', 'namn']

admin.site.register(Uppgift, UppgiftAdmin)

class KravAdmin(admin.ModelAdmin):
    list_display = ['kravid', 'namn', 'myndighet']
    list_filter = ['myndighet']

admin.site.register(Krav, KravAdmin)
