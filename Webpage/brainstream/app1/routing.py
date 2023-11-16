from channels.routing import ProtocolTypeRouter,URLRouter
from django.urls import path
from channels.auth import AuthMiddlewareStack
import os
from django.core.asgi import get_asgi_application
from .consumers import GraphConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path("menu/resultn", GraphConsumer.as_asgi()),
        ])
    )
})