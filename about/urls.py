from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^approaches/$', views.approaches, name='approaches'),
    url(r'^planning/$', views.planning, name='planning'),
]