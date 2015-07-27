from django.contrib import admin
from simplestats.models import Location, Stat


class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')
    list_filter = ('key',)
    date_hierarchy = 'created'


class LocationAdmin(admin.ModelAdmin):
    def _location_url(self, obj):
        return '<a href="{0}">Google Maps</a>'.format(obj.location)
    _location_url.short_description = 'Location'
    _location_url.allow_tags = True

    list_display = ('label', 'created', 'state', '_location_url')
    list_filter = ('label', 'state')
    date_hierarchy = 'created'

admin.site.register(Stat, StatAdmin)
admin.site.register(Location, LocationAdmin)
