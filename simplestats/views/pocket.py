import simplestats.models
import simplestats.requests as requests

from django.conf import settings
from rest_framework.reverse import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import View
from django.contrib import messages


class AuthPocket(View):
    def get(self, request):
        response = requests.post(
            'https://getpocket.com/v3/oauth/request',
            headers={
                'X-Accept': 'application/json',
            },
            json={
                'consumer_key': settings.POCKET_CONSUMER_KEY,
                'redirect_uri': reverse('stats:pocket_confirm', request=request)
            })
        response.raise_for_status()
        code = response.json()['code']
        simplestats.models.Token.objects.create(id='pocket_auth', value=code)
        return redirect(
            'https://getpocket.com/auth/authorize?request_token={token}&redirect_uri={redirect}'.format(
                token=code,
                redirect=reverse('stats:pocket_confirm', request=request),
            ))


class ConfirmPocket(View):
    def get(self, request):
        token = simplestats.models.Token.objects.get(id='pocket_auth')
        response = requests.post(
            'https://getpocket.com/v3/oauth/authorize',
            headers={
                'X-Accept': 'application/json',
            },
            json={
                'consumer_key': settings.POCKET_CONSUMER_KEY,
                'code': token.value,
            })
        response.raise_for_status()
        token.delete()
        code = response.json()
        simplestats.models.Token.objects.create(id='pocket', value=code['access_token'])
        messages.add_message(request, messages.INFO, _('Successfully Authed with Pocket'))
        return redirect('/about')
