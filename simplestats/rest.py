
import json
import logging
from urllib.parse import parse_qs, urlparse

import pytz
from dateutil.parser import parse
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import detail_route
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from simplestats import grafana, models, serializers

from django.shortcuts import get_object_or_404

logger = logging.getLogger(__name__)


class StatsSubView(object):
    @detail_route(methods=['get', 'post'])
    def stats(self, request, slug=None):
        return getattr(self, 'stats_' + request.method)(request, slug)

    def stats_GET(self, request, slug):
        chart = self.get_object()
        queryset = chart.sample_set.order_by('-timestamp')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.SampleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.SampleSerializer(queryset, many=True)
        return Response(serializer.data)

    def stats_POST(self, request, slug):
        chart = self.get_object()
        serializer = serializers.SampleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(key=chart.keys)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class NotesSubView(object):
    @detail_route(methods=['get', 'post'])
    def notes(self, request, slug=None):
        return getattr(self, 'notes_' + request.method)(request, slug)

    def notes_GET(self, request, slug):
        chart = self.get_object()
        queryset = chart.note_set.order_by('-timestamp')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.NoteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.NoteSerialize(queryset, many=True)
        return Response(serializer.data)

    def notes_POST(self, request, slug):
        chart = self.get_object()
        serializer = serializers.NoteSerialize(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(key=chart.keys)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WaypointsSubView(object):
    @detail_route(methods=['get', 'post'])
    def waypoints(self, request, slug=None):
        return getattr(self, 'waypoint_' + request.method)(request, slug)

    def waypoint_GET(self, request, slug):
        chart = self.get_object()
        queryset = chart.note_set.order_by('-timestamp')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.WaypointSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.WaypointSerializer(queryset, many=True)
        return Response(serializer.data)

    def waypoint_POST(self, request, slug):
        chart = self.get_object()
        serializer = serializers.WaypointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(key=chart.keys)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WidgetViewSet(StatsSubView, NotesSubView, WaypointsSubView, grafana.GrafanaWidgetView, viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication, SessionAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    permission_classes = (DjangoModelPermissions,)
    queryset = models.Widget.objects.all()
    serializer_class = serializers.WidgetSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return models.Widget.objects.filter(owner=self.request.user).prefetch_related('meta_set')
        return models.Widget.objects.filter(public=True).prefetch_related('meta_set')

    @detail_route(methods=['post'], permission_classes=[])
    def ifttt(self, request, slug=None):
        location = get_object_or_404(models.Widget, slug=slug)
        body = json.loads(request.body.decode("utf-8"))
        kwargs = {}
        kwargs['state'] = body['state']
        kwargs['description'] = body.get('label')
        kwargs['timestamp'] = parse(body['created'])

        if 'timezone' in body:
            kwargs['timestamp'] = kwargs['timestamp'].replace(tzinfo=pytz.timezone(body['timezone']))

        # Parse out google maps URL and store as lat/lon
        url = urlparse(body['location'])
        qs = parse_qs(url.query)
        kwargs['lat'], kwargs['lon'] = qs['q'][0].split(',')

        movement = location.waypoint_set.create(**kwargs)
        # TODO: Move to a celery job
        location.timestamp = movement.timestamp
        location.save()

        logger.info('Logged movement from ifttt: %s', movement)
        return Response({'status': 'done'})
