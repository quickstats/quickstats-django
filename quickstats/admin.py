from django.contrib import admin
from . import models


class LabelInline(admin.TabularInline):
    model = models.Label


class SettingInline(admin.TabularInline):
    model = models.Setting


class ScrapeInline(admin.TabularInline):
    model = models.Scrape


@admin.register(models.Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "public", "owner", "timestamp", "value")
    list_filter = ("type", ("owner", admin.RelatedOnlyFieldListFilter))
    inlines = [LabelInline, SettingInline, ScrapeInline]


@admin.register(models.Waypoint)
class WaypointAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "body", "lat", "lon", "state")


@admin.register(models.Scrape)
class ScrapeAdmin(admin.ModelAdmin):
    def title(self, obj):
        return obj.widget.title

    list_display = ("title", "driver", "period", "owner")
    list_filter = ("driver", "period", ("owner", admin.RelatedOnlyFieldListFilter))


@admin.register(models.Share)
class ShareAdmin(admin.ModelAdmin):
    def title(self, obj):
        return obj.widget.title

    list_display = ("title", "owner", "created", "viewed")
    list_filter = (("owner", admin.RelatedOnlyFieldListFilter),)
