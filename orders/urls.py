from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^list/orders/$', views.order_list, name='order_list'),
    url(r'^(?P<order_id>\d+)/download/$', views.confirm_payment, name='download'),
    url(r'^(?P<order_id>\d+)/(?P<tx_ref>[\d\w]+)/$', views.order_detail, name='order_detail'),
    url(r'^form/$', views.guest_checkout, name='order_form'),
]
