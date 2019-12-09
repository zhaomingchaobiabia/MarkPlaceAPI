from django.urls import path

from markerplace_develop import views

urlpatterns = [
    path('sales-periods-query/', views.sales_periods_query, name='sales_periods_query'),
    path('pricing-query/', views.pricing_query, name='pricing_query'),
    path('messages_query/', views.messages_query, name='messages_query'),
    path('messages_query_type/', views.messages_query_type, name="messages_query_type"),
    path('message_update', views.message_update, name='message_update'),

    path('test1/', views.test1, name='test1')
]
