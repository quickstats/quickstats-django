
import json
import time

from dateutil.parser import parse
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from simplestats import models

from django.http import JsonResponse


class GrafanaWidgetView(object):
    @action(
        detail=False,
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

    @action(
        detail=False,
        methods=['post'],
        authentication_classes=[BasicAuthentication],
        permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
        )
    def query(self, request):
        '''Grafana Query'''
        body = json.loads(request.body.decode("utf-8"))
        start = parse(body['range']['from'])
        end = parse(body['range']['to'])
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

    @action(detail=False, methods=['post'], authentication_classes=[BasicAuthentication])
    def annotations(self, request):
        '''Grafana annotation'''
        body = json.loads(request.body.decode("utf-8"))
        start = parse(body['range']['from'])
        end = parse(body['range']['to'])
        query = json.loads(body['annotation']['query'])

        klass = query.pop('__model__', 'Note')
        if klass == 'Note':
            qs = models.Note.objects
        if klass == 'Waypoint':
            qs = models.Waypoint.objects
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
