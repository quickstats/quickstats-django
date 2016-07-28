import simplestats.models

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


@admin.register(simplestats.models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')
    list_filter = ('key',)
    date_hierarchy = 'created'


@admin.register(simplestats.models.Annotation)
class AnnotiationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'tags', 'text')


@admin.register(simplestats.models.StatMeta)
class StatMetaAdmin(admin.ModelAdmin):
    list_display = ('chart', 'key', 'value')
    list_filter = ('chart',)


@admin.register(simplestats.models.Countdown)
class CountdownAdmin(admin.ModelAdmin):
    def _icon(self, obj):
        return True if obj.icon else False
    _icon.short_description = _('icon')
    _icon.boolean = True

    def _calendar(self, obj):
        return True if obj.calendar else False
    _calendar.short_description = _('calendar')
    _calendar.boolean = True

    list_display = ('label', 'description', 'created', 'owner', 'public',
                    '_calendar', '_icon', 'repeating', 'allday')
    list_filter = ('owner', 'public',)


@admin.register(simplestats.models.Chart)
class ChartAdmin(admin.ModelAdmin):
    def refresh(self, request, queryset):
        for chart in queryset:
            chart.refresh()

    def _icon(self, obj):
        return True if obj.icon else False
    _icon.short_description = _('icon')
    _icon.boolean = True

    list_display = ('label', 'created', 'owner', 'keys', 'value', 'public',
                    '_icon')
    list_filter = ('owner', 'public',)
    actions = ['refresh']


@admin.register(simplestats.models.Report)
class ReportModel(admin.ModelAdmin):
    list_display = ('date', 'name', 'text')


@admin.register(simplestats.models.Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
