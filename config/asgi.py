"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

# Import ActionCableConsumer directly
try:
    from actioncable import ActionCableConsumer
    has_actioncable = True
except ImportError:
    has_actioncable = False

from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django_asgi_app = get_asgi_application()

if has_actioncable:
    application = ProtocolTypeRouter(
        {
            "http": django_asgi_app,
            "websocket": AllowedHostsOriginValidator(
                AuthMiddlewareStack(
                    URLRouter(
                        [
                            path("cable", ActionCableConsumer.as_asgi()),
                        ]
                    )
                )
            ),
        }
    )
else:
    application = ProtocolTypeRouter(
        {
            "http": django_asgi_app,
        }
    )