from django.conf.urls import patterns, url
from plivoapis import views

urlpatterns = [
    url(r'^inbound/sms$', views.inbound_sms, name='inbound'),
    url(r'^outbound/sms$', views.outbound_sms, name='outbound'),
]
