import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .models import Message
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_user_id = self.scope['url_route']['kwargs']['user_id']
        self.my_id = self.scope['user'].id
        
        # Room name uumuu
        ids = sorted([self.my_id, int(self.other_user_id)])
        self.room_group_name = f'chat_{ids[0]}_{ids[1]}'
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        msg_type = data.get('type', 'message') 
        sender_id = self.my_id

        # 1. Typing Logic
        if msg_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_typing',
                    'typing': data.get('typing', False),
                    'sender_id': sender_id
                }
            )
            return 

        # 2. Message Logic
        message = data.get('message', '')
        image_data = data.get('image', None)
        
        saved_msg = await self.save_message(message, image_data)
        time_now = timezone.localtime(saved_msg.timestamp).strftime('%H:%M')

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'image': saved_msg.image.url if saved_msg.image else None,
                'sender_id': sender_id,
                'timestamp': time_now
            }
        )

    # Browser-itti erguu (Kuni murteessaadha!)
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',  # JavaScript 'data.type === message' kan jedhuun wal simata
            'message': event['message'],
            'image': event['image'],
            'sender_id': event['sender_id'],
            'timestamp': event['timestamp']
        }))

    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'typing': event['typing'],
            'sender_id': event['sender_id']
        }))

    @database_sync_to_async
    def save_message(self, message, image_data):
        other_user = User.objects.get(id=self.other_user_id)
        image_file = None
        if image_data and ';base64,' in image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_file = ContentFile(base64.b64decode(imgstr), name=f'chat_{self.my_id}.{ext}')
        
        return Message.objects.create(
            sender=self.scope['user'], 
            receiver=other_user, 
            content=message, 
            image=image_file
        )