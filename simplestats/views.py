import csv
import itertools
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from simplestats.serializers import LocationSerializer
from rest_framework import permissions, viewsets
from simplestats.models import Location, Stat
import json

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


class LocationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
