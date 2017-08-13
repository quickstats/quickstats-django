import json
import logging

import pytz
from dateutil.parser import parse
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import detail_route
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly)
from rest_framework.response import Response

from simplestats.models import Chart, Countdown, Location, Report, Stat
from simplestats.serializers import (ChartSerializer, CountdownSerializer,
                                     LocationSerializer, ReportSerializer,
                                     StatSerializer)

from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class CountdownViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    permission_classes = (DjangoModelPermissions,)
    queryset = Countdown.objects.all()
    serializer_class = CountdownSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Countdown.objects.filter(owner=self.request.user)
        return Countdown.objects.filter(public=True)


class ChartViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
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

    @detail_route(methods=['get', 'post'])
    def stats(self, request, pk=None):
        return getattr(self, 'stats_' + request.method)(request, pk)

    def stats_GET(self, request, pk):
        chart = self.get_object()
        queryset = self.filter_queryset(Stat.objects.order_by('-created').filter(key=chart.keys))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = StatSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StatSerializer(queryset, many=True)
        return Response(serializer.data)

    def stats_POST(self, request, pk):
        chart = self.get_object()
        serializer = StatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(key=chart.keys)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ReportViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Report.objects.filter(owner_id=self.request.user.id)


class LocationViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @detail_route(methods=['post'], permission_classes=[])
    def ifttt(self, request, pk=None):
        location = get_object_or_404(Location, pk=pk)
        body = json.loads(request.body.decode("utf-8"))
        kwargs = {}
        kwargs['state'] = body['state']
        kwargs['map'] = body['location']
        kwargs['note'] = body.get('label')
        kwargs['created'] = parse(body['created'])
        if 'timezone' in body:
            kwargs['created'] = kwargs['created'].replace(tzinfo=pytz.timezone(body['timezone']))

        movement = location.record(**kwargs)

        logger.info('Logged movement from ifttt: %s', movement)
        return Response({'status': 'done'})

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Location.objects.filter(owner_id=self.request.user.id)
