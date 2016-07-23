from rest_framework import serializers

from simplestats.models import Chart, Countdown, Stat


class CountdownSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Countdown
        fields = ('id', 'created', 'label', 'owner', 'icon')  # , 'calendar')
        read_only_fields = ('id', 'icon',)


class ChartSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Chart
        fields = ('id', 'created', 'label', 'owner', 'value', 'more')


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ('created', 'key', 'value')
