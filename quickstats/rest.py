from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer

from . import models, permissions, serializers

from django.shortcuts import render


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = models.Widget.objects.prefetch_related("owner", "setting_set")
    serializer_class = serializers.WidgetSerializer
    permission_classes = (permissions.IsOwnerOrPublic,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    @action(detail=True, methods=["get"])
    def embed(self, request, pk=None):
        self.object = self.get_object()
        return render(request, "quickstats/widget_embed.html", {"widget": self.object})

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.CanSubscribe]
    )
    def subscribe(self, request, pk=None):
        subscription, created = models.Subscription.objects.get_or_create(
            owner=self.request.user, widget=self.get_object()
        )
        serializer = serializers.SubscriptionSerializer(subscription)
        return Response(serializer.data)


class WaypointViewSet(viewsets.ModelViewSet):
    queryset = models.Waypoint.objects
    serializer_class = serializers.WaypointSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CSVRenderer)

    def get_queryset(self):
        return self.queryset.filter(
            widget=self.kwargs["widget_pk"], widget__owner=self.request.user
        )


class SampleViewSet(viewsets.ModelViewSet):
    queryset = models.Sample.objects
    serializer_class = serializers.SampleSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, CSVRenderer)

    def get_queryset(self):
        return self.queryset.filter(
            widget=self.kwargs["widget_pk"], widget__owner=self.request.user
        )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.prefetch_related("owner", "setting_set")
    serializer_class = serializers.CommmentSerializer

    def get_queryset(self):
        return self.queryset.filter(widget=self.kwargs["widget_pk"])


class SubscriptionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Subscription.objects
    serializer_class = serializers.WidgetSerializer
    permission_classes = (permissions.IsOwner,)

    def get_queryset(self):
        # TODO Fix seralizing as Widget but allowing deleting the subscription
        return models.Widget.objects.filter(
            pk__in=models.Subscription.objects.filter(owner=self.request.user).values_list(
                "widget_id"
            )
        ).prefetch_related("owner", "setting_set")


class CommentViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = models.Comment.objects
    serializer_class = serializers.CommmentSerializer
    permission_classes = (permissions.IsOwner,)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
