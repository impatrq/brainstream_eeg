from django.urls import path

from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='pagina'),
    path('inicio/resultn', views.index, name='resultado'),
    path('inicio/bcin', views.bciin, name='bcii'),
    path('inicio/contacto', views.contactoin, name='contacto'),
    path('inicio/iniciarsesion', views.iniin, name="iniciosesion"),
    path('inicio/acercade', views.acercain, name='acercade'),
]