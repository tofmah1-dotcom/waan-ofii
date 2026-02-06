import os
import django # KANA DABALADHU
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # 'DJANGO_SETTINGS_MODULE' qubee gurguddaan
django.setup() # KANA DABALADHU

import chat.routing # Import kana django.setup() booda ta'uu qaba

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})