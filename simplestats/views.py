import json

from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework import mixins, viewsets

from simplestats.models import Location
from simplestats.serializers import LocationSerializer


class LocationDataTable(View):
    def dateformat(self, date):
        return "Date(%d,%d,%d,%d,%d,%d)" % (
            date.year, date.month - 1, date.day, date.hour, date.minute, date.second)
    def get(self, request):
        dataset = {'cols': [], 'rows': []}
        dataset['cols'].append({'id': 'Location', 'type': 'string'})
        #DDTHH:MM:SS.mmmmmm+HH:MM
        dataset['cols'].append({'id': 'Enter', 'pattern': 'yyyy/MM/dd H:mm:ss', 'type': 'datetime'})
        dataset['cols'].append({'id': 'Exit', 'pattern': 'yyyy/MM/dd H:mm:ss', 'type': 'datetime'})

        locations = {}
        for location in Location.objects.all():
            if location.state == 'entered':
                locations[location.label] = location.created
            elif location.state == 'exited':
                if location.label in locations:
                    entered = locations.pop(location.label)
                    dataset['rows'].append({"c": [
                        {"v": location.label},
                        {"v": self.dateformat(entered), "f":"2015/08/11 17:00:00"},
                        {"v": self.dateformat(location.created), "f":"2015/08/11 17:00:00"},
                    ]})
        response = HttpResponse(content_type='application/json')
        response.write('google.visualization.Query.setResponse(' + json.dumps({
            'version': '0.6',
            'table': dataset,
            'reqId': '0',
            'status': 'ok',
        }) + ');')
        return response

'''
google.visualization.Query.setResponse(
{
    "version":"0.6",
    "reqId":"0",
    "status":"ok",
    "sig":"1049322423",
    "table":{
        "cols":[
            {"id":"A","label":"Location","type":"string"},
            {"id":"B","label":"Entered","type":"datetime","pattern":"yyyy/MM/dd H:mm:ss"},
            {"id":"C","label":"Exited","type":"datetime","pattern":"yyyy/MM/dd H:mm:ss"}
            ],
        "rows":[
            {"c":[
                {"v":"クレール城西"},
                {"v":new Date(2015,7,11,17,0,0),"f":"2015/08/11 17:00:00"},
                {"v":new Date(2015,7,12,13,9,0),"f":"2015/08/12 13:09:00"}
                ]},
            {"c":[{"v":"YMCA"},{"v":new Date(2015,7,11,9,0,0),"f":"2015/08/11 9:00:00"},{"v":new Date(2015,7,11,16,0,0),"f":"2015/08/11 16:00:00"}]},{"c":[{"v":"元気"},{"v":new Date(2015,7,12,17,0,0),"f":"2015/08/12 17:00:00"},{"v":new Date(2015,7,12,22,0,0),"f":"2015/08/12 22:00:00"}]},{"c":[{"v":"クレール城西"},{"v":new Date(2015,7,10,17,0,0),"f":"2015/08/10 17:00:00"},{"v":new Date(2015,7,10,23,9,0),"f":"2015/08/10 23:09:00"}]}]}});
'''


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

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
