import simplestats.models

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
import simplestats.tasks.chart


class LabelInline(admin.TabularInline):
    model = simplestats.models.Label


class MetaInline(admin.TabularInline):
    model = simplestats.models.Meta


@admin.register(simplestats.models.Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('slug', 'timestamp', 'title', 'owner', 'public', 'type')
    list_filter = ('owner', 'public', 'type')
    inlines = [LabelInline, MetaInline]


@admin.register(simplestats.models.Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('created', 'key', 'value')
    list_filter = ('key',)
    date_hierarchy = 'created'


@admin.register(simplestats.models.Annotation)
class AnnotiationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'tags', 'text')


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
            # Call directly (don't queue)
            simplestats.tasks.chart.update_chart(chart.pk)

    def _icon(self, obj):
        return True if obj.icon else False
    _icon.short_description = _('icon')
    _icon.boolean = True

    list_display = ('label', 'created', 'owner', 'keys', 'labels', 'value', 'unit', 'public', '_icon')
    list_filter = ('owner', 'public',)
    actions = ['refresh']


@admin.register(simplestats.models.Report)
class ReportModel(admin.ModelAdmin):
    list_display = ('date', 'name', 'owner', 'text')
    list_filter = ('name', 'owner')


@admin.register(simplestats.models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    list_filter = ('name', 'owner')
