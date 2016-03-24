from rest_framework import permissions, status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.filters import OrderingFilter

from simplestats.models import Chart, Countdown
from simplestats.serializers import ChartSerializer, CountdownSerializer


class CountdownViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    queryset = Countdown.objects.all()
    serializer_class = CountdownSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Countdown.objects.filter(owner=self.request.user)


class ChartViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Chart.objects.filter(owner=self.request.user)
