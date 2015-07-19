from django.contrib import admin
from simplestats.models import Stat


class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')

admin.site.register(Stat, StatAdmin)
