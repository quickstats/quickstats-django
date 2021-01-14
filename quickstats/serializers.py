from rest_framework import serializers

from . import models


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Widget
        fields = (
            "id",
            "owner",
            "title",
            "description",
            "public",
            "icon",
            "value",
            "timestamp",
            "type",
            "meta",
        )

    owner = serializers.ReadOnlyField(source="owner.username")
    type = serializers.ReadOnlyField(source="get_type_display")
    meta = serializers.SerializerMethodField()

    def get_meta(self, obj):
        return {s.name: s.value for s in obj.setting_set.all()}



class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sample
        exclude = ("id", "widget")


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Waypoint
        exclude = ("id", "widget")
