
import json
import logging
from urllib.parse import parse_qs, urlparse

import pytz
from dateutil.parser import parse
from rest_framework import viewsets
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


class SampleViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication, SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    serializer_class = serializers.SampleSerializer

    def get_queryset(self):
        return models.Sample.objects.filter(widget__slug=self.kwargs['widget_slug'])


class NoteViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication, SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    serializer_class = serializers.SampleSerializer

    def get_queryset(self):
        return models.Note.objects.filter(widget__slug=self.kwargs['widget_slug'])


class WaypointViewSet(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication, SessionAuthentication, TokenAuthentication)
    permission_classes = (DjangoModelPermissions,)
    serializer_class = serializers.SampleSerializer

    def get_queryset(self):
        return models.Waypoint.objects.filter(widget__slug=self.kwargs['widget_slug'])


class WidgetViewSet(grafana.GrafanaWidgetView, viewsets.ModelViewSet):
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
