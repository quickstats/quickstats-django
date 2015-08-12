import datetime
import json

from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework import mixins, viewsets
from rest_framework.decorators import list_route

from simplestats.models import Location
from simplestats.serializers import LocationSerializer


class LocationPattern(View):
    def get(self, request):
        response = HttpResponse(content_type='text/plain')
        response.write(json.dumps({
            'created': '{{OccurredAt}}',
            'label': '<label>',
            'state': '{{EnteredOrExited}}',
            'location': '{{LocationMapUrl}} ',
        }))
        return response


class LocationViewSet(
        mixins.CreateModelMixin,
        # mixins.ListModelMixin,
        # mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """
    POST Only View to accept location updates from IFTTT
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    @list_route()
    def datatable(self, request):
        def dateformat(date):
            return "Date(%d,%d,%d,%d,%d,%d)" % (
                date.year, date.month - 1, date.day, date.hour, date.minute, date.second)
        dataset = {'cols': [
            {'id': 'Location', 'label': 'Location', 'type': 'string'},
            {'id': 'Duration', 'label': 'Duration', 'type': 'string'},
            {'id': 'Enter', 'pattern': 'yyyy/MM/dd H:mm:ss', 'type': 'datetime'},
            {'id': 'Exit', 'pattern': 'yyyy/MM/dd H:mm:ss', 'type': 'datetime'},
            {"id": "", "label": "", "pattern": "", "type": "string", "p": {"role": "tooltip"}},
        ], 'rows': []}
        # Later try to get proper tooltips working
        # http://stackoverflow.com/a/11181882/622650

        locations = {}
        for location in Location.objects.filter(created__gte=datetime.datetime.now() - datetime.timedelta(days=7)):
            if location.state == 'entered':
                locations[location.label] = location.created
            elif location.state == 'exited':
                if location.label in locations:
                    entered = locations.pop(location.label)
                    dataset['rows'].append({'c': [
                        {"v": location.label},
                        {"v": str(location.created - entered)},
                        {"v": dateformat(entered)},
                        {"v": dateformat(location.created)},
                        {"v": str(location.created - entered)},
                    ]})

        response = HttpResponse(content_type='application/json')
        response.write('google.visualization.Query.setResponse(' + json.dumps({
            'version': '0.6',
            'table': dataset,
            'reqId': '0',
            'status': 'ok',
        }) + ');')
        return response
