import simplestats.views

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^chart/(?P<uuid>.*)$', simplestats.views.RenderChart.as_view(), name='chart'),
    url(r'^dashboard$', simplestats.views.Dashboard.as_view(), name='dashboard'),
    url(r'^feed$', simplestats.views.LatestEntriesFeed(), name='feed'),

    url(r'^board/usd/jpy/$', simplestats.views.USDJPYBoard.as_view(), name='board_usd_jpy'),
    url(r'^board/wanikani/$', simplestats.views.WaniKaniBoard.as_view(), name='board_wanikani'),
    url(r'^board/weather/fukuoka/temperature/$', simplestats.views.TemperatureBoard.as_view(), name='board_weather_fukuoka_temperature'),
]


def subnav(namespace, request):
    def charts(namespace, request):
        for chart in simplestats.models.Chart.objects.filter(owner=request.user):
            yield chart.label, reverse(namespace + ':chart', kwargs={'uuid': str(chart.id)})
    return {
        _('Charts'): list(charts(namespace, request))
    }
