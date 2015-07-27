from django.contrib import admin
from simplestats.models import Location, Stat


class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')
    list_filter = ('key',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('label', 'created', 'state', 'location')
    list_filter = ('label', 'state')

admin.site.register(Stat, StatAdmin)
admin.site.register(Location, LocationAdmin)
