from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.renderers import JSONRenderer

from . import models, permissions, serializers

from django.shortcuts import render


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = models.Widget.objects.prefetch_related("owner", "setting_set")
    serializer_class = serializers.WidgetSerializer
    permission_classes = (permissions.IsOwnerOrPublic,)

    @action(detail=True, methods=["get"], renderer_classes=(CSVRenderer, JSONRenderer))
    def samples(self, request, pk=None, **kwargs):
        queryset = models.Sample.objects.filter(widget_id=pk)
        serializer = serializers.SampleSerializer(queryset, many=True)
        return Response(serializer.data)

    @samples.mapping.post
    def samples_post(self, request, pk=None):
        pass

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        queryset = models.Comment.objects.filter(widget_id=pk)
        serializer = serializers.CommmentSerializer(queryset, many=True)
        return Response(serializer.data)

    @comments.mapping.post
    def comments_post(self, request, pk=None):
        pass

    @samples.mapping.put
    def samples_put(self, request, pk=None):
        pass

    @action(detail=True, methods=["get"])
    def embed(self, request, pk=None):
        self.object = self.get_object()
        return render(request, "quickstats/widget_embed.html", {"widget": self.object})


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
