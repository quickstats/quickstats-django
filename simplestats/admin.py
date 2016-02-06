import simplestats.models
import simplestats.signals

from django.contrib import admin


class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')
    list_filter = ('key',)
    date_hierarchy = 'created'

admin.site.register(simplestats.models.Stat, StatAdmin)
admin.site.register(simplestats.models.Countdown)
