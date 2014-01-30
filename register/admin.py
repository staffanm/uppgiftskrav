from django.contrib import admin
from register.models import Uppgift, Krav
# Register your models here.
class UppgiftAdmin(admin.ModelAdmin):
    pass
admin.site.register(Uppgift, UppgiftAdmin)

class KravAdmin(admin.ModelAdmin):
    pass
admin.site.register(Krav, KravAdmin)
