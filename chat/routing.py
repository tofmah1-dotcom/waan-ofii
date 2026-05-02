from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # group_id qofa (lakkoofsa)
    re_path(r'ws/chat/group/(?P<group_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
    
    # room_name (qubee, lakkoofsa, sarara-xiqqaa fi sarara-jallaa kan fudhatu)
    # Mallattoon [\w.-]+ jedhu baay'ee murteessaadha!
    re_path(r'ws/chat/(?P<room_name>[\w.-]+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_name>[\w._-]+)/$', consumers.ChatConsumer.as_asgi()),
]