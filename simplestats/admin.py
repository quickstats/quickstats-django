import simplestats.models

from django.contrib import admin


class LabelInline(admin.TabularInline):
    model = simplestats.models.Label


class MetaInline(admin.TabularInline):
    model = simplestats.models.Meta


@admin.register(simplestats.models.Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'timestamp', 'title', 'owner', 'public', 'type')
    list_filter = ('owner', 'public', 'type')
    inlines = [LabelInline, MetaInline]
    ordering = ['-timestamp']


@admin.register(simplestats.models.Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'title', 'description')
    list_filter = ('widget__owner', 'widget__public')
    ordering = ['-timestamp']


@admin.register(simplestats.models.Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'lat', 'lon', 'state', 'description')
    list_filter = ('widget__owner', 'widget__public', 'state')
    ordering = ['-timestamp']
