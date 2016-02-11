from rest_framework import serializers

from simplestats.models import Chart, Countdown


class CountdownSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Countdown
        fields = ('created', 'label')  # , 'calendar', 'owner')


class ChartSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Chart
        fields = ('created', 'label')  # , 'calendar', 'owner')
