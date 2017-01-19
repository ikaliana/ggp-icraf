from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^driver_lulc/$', views.driver_lulc, name='driver_lulc'),
    url(r'^emission/$', views.emission, name='emission'),
    url(r'^sequestration/$', views.sequestration, name='sequestration'),
    url(r'^peat/$', views.peat, name='peat'),
    url(r'^economic/$', views.economic, name='economic'),
    url(r'^lup/$', views.lup, name='lup'),
    url(r'^valuechain/$', views.valuechain, name='valuechain'),
    url(r'^land_requirement/$', views.land_requirement, name='land_requirement'),
    url(r'^suitability/$', views.suitability, name='suitability'),
    url(r'^hcv/$', views.hcv, name='hcv'),
    url(r'^rpjmd/$', views.rpjmd, name='rpjmd'),
    url(r'^rtrw/$', views.rtrw, name='rtrw'),
    url(r'^ccm/$', views.ccm, name='ccm'),
    url(r'^lrp/$', views.lrp, name='lrp'),
]