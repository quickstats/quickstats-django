from django.contrib import admin
from . import models


class LabelInline(admin.TabularInline):
    model = models.Label


@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("widget", "owner")
    list_filter = (("owner", admin.RelatedOnlyFieldListFilter),)


@admin.register(models.Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "public", "owner")
    list_filter = ("type", "public", ("owner", admin.RelatedOnlyFieldListFilter))
    inlines = [LabelInline]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "owner")
