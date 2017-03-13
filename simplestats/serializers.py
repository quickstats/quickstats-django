from rest_framework import serializers

from simplestats.models import Chart, Countdown, Location, Report, Stat


class CountdownSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Countdown
        fields = ('id', 'created', 'label', 'owner', 'icon', 'more', 'description')
        read_only_fields = ('id', 'icon',)


class ChartSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Chart
        fields = ('id', 'created', 'label', 'owner', 'value', 'icon', 'more', 'unit', 'public')
        read_only_fields = ('id', 'icon',)


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ('created', 'key', 'value')


class ReportSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Report
        fields = ('date', 'name', 'text', 'url')


class LocationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Location
        fields = ('id', 'name', 'owner')
        read_only_fields = ('id',)
