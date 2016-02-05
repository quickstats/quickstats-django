from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

import simplestats.views

urlpatterns = [
    url(r'^usd/jpy/$', simplestats.views.USDJPY.as_view(), name='usd_jpy'),
]


def subnav(namespace, request):
    if request.user.is_authenticated():
        return {
            _('Charts'): [
                (_('USD/JPY'), reverse(namespace + ':usd_jpy'))
            ]
        }
