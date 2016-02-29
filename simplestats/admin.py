import simplestats.models
import simplestats.signals

from django.contrib import admin


@admin.register(simplestats.models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')
    list_filter = ('key',)
    date_hierarchy = 'created'


@admin.register(simplestats.models.Countdown)
class CountdownAdmin(admin.ModelAdmin):
    list_display = ('label', 'created', 'owner', 'public', 'calendar')
    list_filter = ('owner', 'public',)


@admin.register(simplestats.models.Chart)
class ChartAdmin(admin.ModelAdmin):
    list_display = ('label', 'created', 'owner', 'keys')
