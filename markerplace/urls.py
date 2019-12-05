from django.contrib import admin
from django.urls import path
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
    path('order-update/', views.order_update, name='order_update'),
    path('carriers-update-accept/', views.carriers_update_accept, name='carriers_update_accept'),

    path('carriers-query/', views.carriers_query, name='carriers_query'),
]
