from django.urls import path

from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('inicio', views.inicio, name='inicio'),
    path('resultn', views.result, name='resultado'),
    path('bcin', views.bciin, name='bcii'),
    path('contacto', views.contactoin, name='contacto'),
    path('acercade', views.acercain, name='acercade'),
    path('cognitive', views.cognitive, name='cognitive'),
]