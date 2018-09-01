from rest_framework import serializers

from simplestats import models


# Custom seralizer field so that empty 'more' links are returned as None instead of empty string
class CustomURLField(serializers.URLField):
    def to_representation(self, value):
        if not value:
            return None
        return value


class WidgetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    meta = serializers.SerializerMethodField()
    more = CustomURLField()

    def get_meta(self, obj):
        return {
            x.key: x.value for x in obj.meta_set.filter(output=True)
        }

    class Meta:
        model = models.Widget
        exclude = ('id',)
        read_only_fields = ('owner', 'icon', 'meta')


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sample
        fields = ('timestamp', 'value')
