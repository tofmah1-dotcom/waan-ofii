from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Koodiin kun space fi maqaa dheeraa hunda makiinaa kee barsiisa
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]