from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^testcsv/$', views.testcsv, name='TestCSV'),
    url(r'^geojson/$', views.testgeojson, name='GeoJson'),
]