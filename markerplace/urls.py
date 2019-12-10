from django.contrib import admin
from django.urls import path, re_path
from markerplace import views

urlpatterns = [
    path('', views.index, name='index'),
    path('offers-update/', views.offers_update, name='offers_update'),
    path('batch-status/', views.batch_status, name='batch_status'),
    path('offers-query/', views.offers_query, name='offers_query'),
    path('offers-query-date/', views.offers_query_date, name='offers_query_date'),
    path('offers-query-quantity/', views.offers_query_quantity, name='offers_query_quantity'),
    path('batch-query/', views.batch_query, name='batch_query'),
    path('orders-query/', views.orders_query, name='orders_query'),
    path('orders-query-date/', views.orders_query_date, name='orders_query_date'),
    path('orders-query-id/', views.orders_query_id, name='orders_query_id'),
    path('orders-update/', views.orders_update, name='orders_update'),
    path('orders-update-accept/', views.orders_update_accept, name='orders_update_accept'),
    path('carriers-query/', views.carriers_query, name='carriers_query'),
    path('orders-query-id/', views.orders_query_id, name='orders_query_id'),
    path('order-comments-query/', views.order_comments_query, name='order_comments_query'),
    path('order_comments_query_date/', views.order_comments_query_date, name='order_comments_query_date'),
    path('order-comments-query-id/', views.order_comments_query_id, name='order_comments_query_id'),
    path('client-order-comments-update/', views.client_order_comments_update, name='client_order_comments_update'),
    path('incidents-query/', views.incidents_query, name='incidents_query'),
    path('incident-update/', views.incident_update, name='incident_update'),
    re_path(r'^order/(.+)/$', views.order),
    re_path(r'^order-shop/(.+)/$', views.order_shop),
]
