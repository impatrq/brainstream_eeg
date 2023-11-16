"""
ASGI config for breainstream project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter, URLRouter
# from app1.routing import ws_urlpatterns
from channels.auth import AuthMiddlewareStack
import os
from django.core.asgi import get_asgi_application


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'breainstream.settings')

# application = ProtocolTypeRouter(
#     {
#         # "http": get_asgi_application(),
#         "websocket": AuthMiddlewareStack(
#             URLRouter(
#                 ws_urlpatterns
#             )
#         )
#     }
# )
