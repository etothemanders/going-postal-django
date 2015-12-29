from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^load_geojson/$', views.load_geojson, name='load_geojson'),
    url(r'^settings/$', views.user_settings, name='settings'),
    url(r'^shipments/$', views.shipments, name='shipments'),
    url(r'^shipments/add/$', views.add_shipment, name='add_shipment'),
    url(r'^shipments/delete/$', views.delete_shipment, name='delete_shipment')
]
