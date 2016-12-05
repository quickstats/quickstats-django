import simplestats.feed
import simplestats.views
import simplestats.grafana

from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^$', simplestats.views.Dashboard.as_view(), name='dashboard'),
    url(r'^keys/$', simplestats.views.KeysList.as_view(), name='keys'),
    url(r'^graph/(?P<key>.*)$', simplestats.views.Graph.as_view(), name='graph'),
    url(r'^chart/(?P<uuid>.*)$', simplestats.views.RenderChart.as_view(), name='chart'),
    url(r'^board/(?P<uuid>.*)$', simplestats.views.RenderBoard.as_view(), name='board'),

    url(r'report/$', simplestats.views.ReportList.as_view(), name='report-list'),
    url(r'report/(?P<pk>.*)$', simplestats.views.ReportDetail.as_view(), name='report-detail'),

    url(r'^feed$', simplestats.feed.LatestEntriesFeed(), name='feed'),

    url(r'^grafana$', simplestats.grafana.Index.as_view()),
    url(r'^grafana/query$', simplestats.grafana.Query.as_view()),
    url(r'^grafana/search$', simplestats.grafana.Search.as_view()),
    url(r'^grafana/annotations$', simplestats.grafana.Annotations.as_view()),
]


def subnav(namespace, request):
    return {
        _('Charts'): [
            (_('Index'), reverse(namespace + ':keys')),
            (_('Dashboard'), reverse(namespace + ':dashboard')),
            (_('Reports'), reverse(namespace + ':report-list')),
        ]
    }
