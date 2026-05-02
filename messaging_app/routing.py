from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Garaa garummaa 'user_id' fi 'username' gidduu jiru hubadhu
    # JavaScript kee consumers.py irratti 'user_id' waan eeguuf lakkoofsa eega
    re_path(r'ws/chat/(?P<user_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]