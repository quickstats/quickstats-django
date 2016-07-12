import simplestats.feed
import simplestats.views
import simplestats.views.grafana as grafana
import simplestats.views.pocket as pocket

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^$', simplestats.views.KeysList.as_view(), name='keys'),
    url(r'^graph/(?P<key>.*)$', simplestats.views.Graph.as_view(), name='graph'),
    url(r'^chart/(?P<uuid>.*)$', simplestats.views.RenderChart.as_view(), name='chart'),
    url(r'^board/(?P<uuid>.*)$', simplestats.views.RenderBoard.as_view(), name='board'),

    url(r'^dashboard$', simplestats.views.Dashboard.as_view(), name='dashboard'),
    url(r'^feed$', simplestats.feed.LatestEntriesFeed(), name='feed'),

    url(r'^grafana$', grafana.Index.as_view()),
    url(r'^grafana/query$', grafana.Query.as_view()),
    url(r'^grafana/search$', grafana.Search.as_view()),
    url(r'^grafana/annotations$', grafana.Annotations.as_view()),

    url(r'^pocket/auth', pocket.AuthPocket.as_view()),
    url(r'^pocket/confirm', pocket.ConfirmPocket.as_view(), name='pocket_confirm'),
]


def subnav(namespace, request):
    def charts(namespace, request):
        yield _('Index'), reverse(namespace + ':keys')
        for chart in simplestats.models.Chart.objects.filter(owner=request.user.id):
            yield chart.label, reverse(namespace + ':chart', kwargs={'uuid': str(chart.id)})
    return {
        _('Charts'): list(charts(namespace, request))
    }
