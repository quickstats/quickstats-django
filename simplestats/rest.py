#from pomodoro.permissions import IsOwner
from rest_framework import permissions, status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)

from simplestats.models import Chart, Countdown
from simplestats.serializers import ChartSerializer, CountdownSerializer


class CountdownViewSet(viewsets.ModelViewSet):
    queryset = Countdown.objects.all()
    serializer_class = CountdownSerializer
    #permission_classes = (IsOwner,)
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Countdown.objects.filter(owner=self.request.user)


class ChartViewSet(viewsets.ModelViewSet):
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Chart.objects.filter(owner=self.request.user)
