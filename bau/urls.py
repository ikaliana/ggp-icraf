from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lulc/$', views.lulc, name='lulc_base'),
    url(r'^lulc/(?P<landcover>.*)/(?P<period>.*)$', views.lulc, name='lulc'),
    url(r'^lulc-model/$', views.lulc_model, name='lulc_model'),
    url(r'^driver/$', views.driver, name='driver'),
    url(r'^carbon-emission/$', views.carbon_emission, name='carbon_emission_base'),
    url(r'^carbon-emission/(?P<period>.*)$', views.carbon_emission, name='carbon_emission'),
    url(r'^carbon-sequestration/$', views.carbon_sequestration, name='carbon_sequestration_base'),
    url(r'^carbon-sequestration/(?P<period>.*)$', views.carbon_sequestration, name='carbon_sequestration'),
    url(r'^carbon-peat/$', views.carbon_peat, name='carbon_peat_base'),
    url(r'^carbon-peat/(?P<period>.*)$', views.carbon_peat, name='carbon_peat'),
    url(r'^biodiversity-difa/$', views.biodiversity_difa, name='biodiversity_difa'),
    # url(r'^biodiversity-sequestration/$', views.biodiversity_sequestration, name='biodiversity_sequestration'),
    url(r'^biodiversity-teci/$', views.biodiversity_teci, name='biodiversity_teci'),
    url(r'^hydrology-sedimentasi/$', views.hydrology_sedimentasi, name='hydrology_sedimentasi'),
    url(r'^hydrology-runoff/$', views.hydrology_runoff, name='hydrology_runoff'),
    url(r'^economic-regional/$', views.economic_regional, name='economic_regional'),
    url(r'^economic-profitability/$', views.economic_profitability, name='economic_profitability_base'),
    url(r'^economic-profitability/(?P<period>.*)$', views.economic_profitability, name='economic_profitability'),
    url(r'^market/$', views.market, name='market'),
    url(r'^issue/$', views.issue, name='issue'),
]