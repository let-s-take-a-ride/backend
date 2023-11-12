import os
from configurations.asgi import get_asgi_application
from configurations import importer
from channels.routing import ProtocolTypeRouter, URLRouter
from consumers import ChatConsumer
from django.urls import re_path
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

importer.install()

django_asgi_app = get_asgi_application()

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat", ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)

