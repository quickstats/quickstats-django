from rest_framework import serializers

from . import models


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Widget
        fields = "__all__"


class CommmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = "__all__"


class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Series
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sample
        fields = ("timestamp", "value")
