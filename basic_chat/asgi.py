"""
ASGI config for basic_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter

import chat.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basic_chat.settings')
django.setup()

application = ProtocolTypeRouter({
    "http":get_asgi_application(),
    "websocket":AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatters
        )
    ),
})

# application = get_asgi_application()
