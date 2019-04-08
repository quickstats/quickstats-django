import logging

import json
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.http import JsonResponse


from . import models

logger = logging.getLogger(__name__)


class Search(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        print(query)
        return JsonResponse({})


class Query(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        print(query)
        return JsonResponse({})


class Annotations(LoginRequiredMixin, View):
    def post(self, request, **kwargs):
        query = json.loads(request.body.decode("utf8"))
        print(query)
        return JsonResponse({})
