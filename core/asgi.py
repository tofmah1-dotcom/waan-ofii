import os
import django
from django.core.asgi import get_asgi_application

# 1. OS environment jalqaba qindeessi
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# 2. Django Setup jalqaba haa hojjetu
django.setup()

# 3. HTTP application uumi
django_asgi_app = get_asgi_application()

# 4. Channels imports Setup booda ta'uu qabu
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing 

application = ProtocolTypeRouter({
    # HTTP requests
    "http": django_asgi_app,
    
    # WebSocket requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})