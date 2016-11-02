from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^carbon/$', views.carbon, name='carbon'),
    url(r'^biodiversity/$', views.biodiversity, name='biodiversity'),
    url(r'^hydrology/$', views.hydrology, name='hydrology'),
    url(r'^lulc/$', views.lulc, name='lulc'),
    url(r'^economic/$', views.economic, name='economic'),
    url(r'^lup/$', views.lup, name='lup'),
]