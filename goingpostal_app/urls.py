from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^gmail/add/$', views.add_gmail, name='add_gmail'),
    url(r'^gmail/delete/$', views.delete_gmail, name='delete_gmail'),
    url(r'^gmail/handle-auth-response/$', views.handle_gmail_auth_response, name='handle_gmail_auth_response'),
    url(r'^load_geojson/$', views.load_geojson, name='load_geojson'),
    url(r'^settings/$', views.user_settings, name='settings'),
    url(r'^shipments/$', views.shipments, name='shipments'),
    url(r'^shipments/add/$', views.add_shipment, name='add_shipment'),
    url(r'^shipments/delete/$', views.delete_shipment, name='delete_shipment'),
    url(r'^user/delete/$', views.delete_user, name='delete_user')
]
