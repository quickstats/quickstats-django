from rest_framework import serializers

from . import models


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Widget
        fields = (
            "id",
            "owner",
            "name",
            "description",
            "public",
            "value",
            "type",
            "formatter",
            "formatted",
        )

    owner = serializers.ReadOnlyField(source="owner.username")
    type = serializers.ReadOnlyField(source="get_type_display")


class CommmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sample
        fields = ("timestamp", "value")
