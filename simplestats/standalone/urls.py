"""standalone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from rest_framework import routers

import simplestats.rest as rest

from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

router = routers.DefaultRouter(trailing_slash=False)
router.register('chart', rest.ChartViewSet)
router.register('countdown', rest.CountdownViewSet)

urlpatterns = [
    url('', include('simplestats.urls')),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls')),
    url(r'^about', TemplateView.as_view(template_name="about.html")),
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain')),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^admin/', admin.site.urls),
]