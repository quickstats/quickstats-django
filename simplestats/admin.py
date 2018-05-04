import simplestats.models

from django.contrib import admin
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
