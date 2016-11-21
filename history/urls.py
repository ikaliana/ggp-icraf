from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lulc/$', views.lulc, name='lulc_base'),
    url(r'^lulc/(?P<landcover>.*)/(?P<period>.*)$', views.lulc, name='lulc'),
    url(r'^driver/$', views.driver, name='driver'),
    url(r'^carbon-emission/$', views.carbon_emission, name='carbon_emission'),
    url(r'^carbon-sequestration/$', views.carbon_sequestration, name='carbon_sequestration'),
    url(r'^carbon-peat/$', views.carbon_peat, name='carbon_peat'),
    url(r'^biodiversity-emission/$', views.biodiversity_emission, name='biodiversity_emission'),
    url(r'^biodiversity-sequestration/$', views.biodiversity_sequestration, name='biodiversity_sequestration'),
    url(r'^biodiversity-peat/$', views.biodiversity_peat, name='biodiversity_peat'),
    url(r'^hydrology/$', views.hydrology, name='hydrology'),
    url(r'^economic-regional/$', views.economic_regional, name='economic_regional'),
    url(r'^economic-profitability/$', views.economic_profitability, name='economic_profitability'),
    url(r'^market/$', views.market, name='market'),
    url(r'^issue/$', views.issue, name='issue'),
]