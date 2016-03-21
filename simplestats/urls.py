import simplestats.views

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^usd/jpy/$', simplestats.views.USDJPY.as_view(), name='usd_jpy'),
    url(r'^wanikani/$', simplestats.views.WaniKani.as_view(), name='wanikani'),

    url(r'^weather/fukuoka/temperature/$', simplestats.views.Temperature.as_view(), name='weather_fukuoka_temperature'),
    url(r'^dashboard$', simplestats.views.Dashboard.as_view(), name='dashboard'),
    url(r'^feed$', simplestats.views.LatestEntriesFeed(), name='feed'),

    url(r'^board/usd/jpy/$', simplestats.views.USDJPYBoard.as_view(), name='board_usd_jpy'),
    url(r'^board/wanikani/$', simplestats.views.WaniKaniBoard.as_view(), name='board_wanikani'),
    url(r'^board/weather/fukuoka/temperature/$', simplestats.views.TemperatureBoard.as_view(), name='board_weather_fukuoka_temperature'),
]


def subnav(namespace, request):
    return {
        _('Charts'): [
            (_('Dashboard'), reverse(namespace + ':dashboard')),
            (_('USD/JPY'), reverse(namespace + ':usd_jpy')),
            (_('Temperature'), reverse(namespace + ':weather_fukuoka_temperature')),
            (_('Wani Kani'), reverse(namespace + ':wanikani')),
        ]
    }
