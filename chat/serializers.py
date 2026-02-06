from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    username = serializers.ReadOnlyField(source='user.username') # Username dabalachuun gaariidha

    class Meta:
        model = Message
        # 'image' fi 'audio' asitti dabalameera
        fields = ['id', 'user', 'username', 'user_email', 'room_name', 'content', 'image', 'audio', 'timestamp']