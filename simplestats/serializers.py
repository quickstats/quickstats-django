from rest_framework import serializers

from simplestats.models import Countdown


class CountdownSerializer(serializers.ModelSerializer):
    #owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Countdown
        fields = ('created', 'label')  # , 'calendar', 'owner')
