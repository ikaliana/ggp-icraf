from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^drivers/$', views.drivers, name='drivers'),
    url(r'^landuse/$', views.landuse, name='landuse'),
    url(r'^env-carbon/$', views.env_carbon, name='env-carbon'),
    url(r'^env-biodiversity/$', views.env_biodiversity, name='env-biodiversity'),
    url(r'^env-hydrology/$', views.env_hydrology, name='env-hydrology'),
    url(r'^eco-regional/$', views.eco_regional, name='eco-regional'),
    url(r'^eco-profit/$', views.eco_profit, name='eco-profit'),
    url(r'^suitability/$', views.suitability, name='suitability'),
    url(r'^hcv/$', views.hcv, name='hcv'),
    url(r'^hcs/$', views.hcs, name='hcs'),
    url(r'^dev-plan/$', views.dev_plan, name='dev-plan'),
    # url(r'^ccm/$', views.ccm, name='ccm'),
    # url(r'^lrp/$', views.lrp, name='lrp'),
    # url(r'^valuechain/$', views.valuechain, name='valuechain'),
    # url(r'^land_requirement/$', views.land_requirement, name='land_requirement'),
]