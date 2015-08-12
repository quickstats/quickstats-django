import simplestats.views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^location$', simplestats.views.LocationPattern.as_view(), name='location'),
    url(r'^datatable$', simplestats.views.LocationDataTable.as_view(), name='locationdatatable'),
)
