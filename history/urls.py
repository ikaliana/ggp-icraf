from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lulc/(?P<commodity_name>.*)$', views.lulc, name='lulc'),
    url(r'^test/$', views.test, name='test'),
]