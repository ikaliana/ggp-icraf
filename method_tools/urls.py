from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^environmental/$', views.environmental, name='environmental'),
    url(r'^lulc/$', views.lulc, name='lulc'),
    url(r'^economic/$', views.economic, name='economic'),
]