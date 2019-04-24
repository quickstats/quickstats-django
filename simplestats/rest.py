from rest_framework import viewsets
from rest_framework.decorators import action
from . import models, serializers
from django.shortcuts import render


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = models.Widget.objects
    serializer_class = serializers.WidgetSerializer

    @action(detail=True, methods=["get"])
    def samples(self, request, pk=None):
        pass

    @samples.mapping.post
    def samples_post(self, request, pk=None):
        pass

    @samples.mapping.put
    def samples_put(self, request, pk=None):
        pass

    @action(detail=True, methods=["get"])
    def embed(self, request, pk=None):
        self.object = self.get_object()
        return render(request, "simplestats/widget.embed.html", {"widget": self.object})


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = models.Subscription.objects
    serializer_class = serializers.SubscriptionSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects
    serializer_class = serializers.CommmentSerializer
