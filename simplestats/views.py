import json

from django.http import HttpResponse
from django.views.generic.base import View
from rest_framework import mixins, viewsets

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

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
