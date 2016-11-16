from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lulc/$', views.lulc, name='lulc_base'),
    url(r'^lulc/(?P<landcover>.*)/(?P<period>.*)$', views.lulc, name='lulc'),
    url(r'^environmental/$', views.environmental, name='environmental'),
    url(r'^economic/$', views.economic, name='economic'),
    url(r'^market/$', views.market, name='market'),
    url(r'^issue/$', views.issue, name='issue'),
]