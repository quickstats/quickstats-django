from rest_framework import viewsets
from rest_framework.decorators import action
from . import models, serializers


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = models.Widget.objects
    serializer_class = serializers.WidgetSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = models.Subscription.objects
    serializer_class = serializers.SubscriptionSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects
    serializer_class = serializers.CommmentSerializer


class SeriesViewSet(viewsets.ModelViewSet):
    queryset = models.Series.objects
    serializer_class = serializers.SeriesSerializer

    @action(detail=True, methods=["get"])
    def samples(self, request, pk=None):
        pass

    @samples.mapping.post
    def samples_post(self, request, pk=None):
        pass

    @samples.mapping.put
    def samples_put(self, request, pk=None):
        pass
