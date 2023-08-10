from django.urls import path

from .consumers import GraphConsumer

ws_urlpatterns = [
    path("menu/resultn", GraphConsumer.as_asgi()),
]
