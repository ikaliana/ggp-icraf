from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^driver_lulc/$', views.driver_lulc, name='driver_lulc'),
    url(r'^environmental_services/$', views.environmental_services, name='environmental_services'),
    url(r'^economic_impact/$', views.economic_impact, name='economic_impact'),
    url(r'^land_requirement/$', views.land_requirement, name='land_requirement'),
    url(r'^land_supply/$', views.land_supply, name='land_supply'),
    url(r'^development_plan/$', views.development_plan, name='development_plan'),
    url(r'^other_plan/$', views.other_plan, name='other_plan'),
]