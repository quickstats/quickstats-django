from rest_framework import viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from rest_framework.permissions import (DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly)

from simplestats.models import Chart, Countdown, Stat
from simplestats.serializers import (ChartSerializer, CountdownSerializer,
                                     StatSerializer)


class CountdownViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Countdown.objects.all()
    serializer_class = CountdownSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Countdown.objects.filter(owner=self.request.user)
        return Countdown.objects.filter(public=True)


class ChartViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Chart.objects.all()
    serializer_class = ChartSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Chart.objects.filter(owner=self.request.user)
        return Chart.objects.filter(public=True)


class StatViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('key',)
    permission_classes = (DjangoModelPermissions,)
    queryset = Stat.objects.all()
    serializer_class = StatSerializer
