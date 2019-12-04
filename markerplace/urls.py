from django.contrib import admin
from django.urls import path
from markerplace import views
urlpatterns = [
    path('', views.index, name='index')
]
