import datetime
import json
import logging
import time
from urllib.parse import parse_qs, urlparse

import pytz
from dateutil.parser import parse
from rest_framework import status, viewsets
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import detail_route, list_route
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (DjangoModelPermissions,
                                        DjangoModelPermissionsOrAnonReadOnly)
from rest_framework.response import Response

from simplestats.models import Note, Waypoint, Widget
from simplestats.serializers import SampleSerializer, WidgetSerializer

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware

logger = logging.getLogger(__name__)
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class WidgetViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    filter_backends = (OrderingFilter,)
    permission_classes = (DjangoModelPermissions,)
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return Widget.objects.filter(owner=self.request.user).prefetch_related('meta_set')
        return Widget.objects.filter(public=True).prefetch_related('meta_set')

    @detail_route(methods=['get', 'post'])
    def stats(self, request, slug=None):
        return getattr(self, 'stats_' + request.method)(request, slug)

    def stats_GET(self, request, slug):
        chart = self.get_object()
        queryset = chart.sample_set.order_by('-timestamp')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SampleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SampleSerializer(queryset, many=True)
        return Response(serializer.data)

    def stats_POST(self, request, slug):
        chart = self.get_object()
        serializer = SampleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(key=chart.keys)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
        )
    def search(self, request):
        '''Grafana Search'''
        query = json.loads(request.body.decode("utf-8"))

        qs = self.get_queryset()\
            .filter(label__name='metric', label__value__contains=query['target'])\
            .values_list('label__value', flat=True).distinct('label__value')

        return JsonResponse(list(qs), safe=False)

    def __ts(self, ts):
        return time.mktime(ts.timetuple()) * 1000

    @list_route(
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
        )
    def query(self, request):
        '''Grafana Query'''
        body = json.loads(request.body.decode("utf-8"))
        start = make_aware(
            datetime.datetime.strptime(body['range']['from'], DATETIME_FORMAT),
            pytz.utc)
        end = make_aware(
            datetime.datetime.strptime(body['range']['to'], DATETIME_FORMAT),
            pytz.utc)
        results = []

        targets = [target['target'] for target in body['targets']]
        for widget in self.get_queryset()\
                .filter(label__name='metric', label__value__in=targets):
            response = {
                'target': widget.title,
                # 'target': str({l.name: l.value for l in widget.label_set.all()}),
                'datapoints': []
            }
            for dp in widget.sample_set.filter(timestamp__gte=start, timestamp__lte=end).order_by('timestamp'):
                response['datapoints'].append([
                    dp.value,
                    self.__ts(dp.timestamp)
                ])
            results.append(response)
        return JsonResponse(results, safe=False)

    @list_route(methods=['post'], authentication_classes=[BasicAuthentication])
    def annotations(self, request):
        '''Grafana annotation'''
        body = json.loads(request.body.decode("utf-8"))
        start = make_aware(
            datetime.datetime.strptime(body['range']['from'], DATETIME_FORMAT),
            pytz.utc)
        end = make_aware(
            datetime.datetime.strptime(body['range']['to'], DATETIME_FORMAT),
            pytz.utc)
        query = json.loads(body['annotation']['query'])

        klass = query.pop('__model__', 'Note')
        if klass == 'Note':
            qs = Note.objects
        if klass == 'Waypoint':
            qs = Waypoint.objects
            if 'state' in query:
                qs = qs.filter(state=query.pop('state'))

        # Make sure we only get notes from widgets that our user owns
        qs = qs.filter(widget__owner=request.user)
        # Then loop through our query items to compare against labels

        for k, v in query.items():
            qs = qs.filter(widget__label__name=k, widget__label__value=v)

        results = []
        for annotation in qs\
                .order_by('timestamp')\
                .filter(timestamp__gte=start)\
                .filter(timestamp__lte=end):
            if klass == 'Note':
                results.append({
                    'annotation': body['annotation']['name'],
                    'time': self.__ts(annotation.timestamp),
                    'title': annotation.title,
                    'tags': [
                        '{x.name}:{x.value}'.format(x=x) for x in annotation.widget.label_set.all()
                        ],
                    'text': annotation.description,
                    })
            if klass == 'Waypoint':
                results.append({
                    'annotation': body['annotation']['name'],
                    'time': self.__ts(annotation.timestamp),
                    'title': annotation.state,
                    'tags': [
                        '{x.name}:{x.value}'.format(x=x) for x in annotation.widget.label_set.all()
                        ],
                    'text': annotation.description,
                    })

        return JsonResponse(results, safe=False)

    @detail_route(methods=['post'], permission_classes=[])
    def ifttt(self, request, slug=None):
        location = get_object_or_404(Widget, slug=slug)
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
