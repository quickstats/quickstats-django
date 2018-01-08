from rest_framework import serializers

from simplestats.models import Chart, Countdown, Data, Location, Report, Stat, Widget


class WidgetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Widget
        fields = '__all__'
        read_only_fields = ('owner', 'icon',)


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


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('timestamp', 'value')


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
