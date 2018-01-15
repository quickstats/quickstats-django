from rest_framework import serializers

from simplestats import models


class WidgetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = models.Widget
        exclude = ('id',)
        read_only_fields = ('owner', 'icon',)


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sample
        fields = ('timestamp', 'value')
