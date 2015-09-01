from django.contrib import admin
from simplestats.models import Stat


class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')
    list_filter = ('key',)
    date_hierarchy = 'created'

admin.site.register(Stat, StatAdmin)
