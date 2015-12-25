from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^shipments/$', views.shipments, name='shipments'),
    url(r'^shipments/add/$', views.add_shipment, name='add_shipment'),
    url(r'^shipments/delete/$', views.delete_shipment, name='delete_shipment'),
    url(r'^load_geojson/$', views.load_geojson, name='load_geojson'),
]
