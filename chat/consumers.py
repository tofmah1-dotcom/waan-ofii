import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 1. Maqaa room URL irraa fiduu
        raw_room_name = self.scope['url_route']['kwargs']['room_name']
        
        # 2. Maqaa garee qulqulleessuu (Space gara sarara - tti)
        clean_room_name = re.sub(r'[^a-zA-Z0-9._-]', '-', raw_room_name)
        
        self.room_name = clean_room_name
        self.room_group_name = f'chat_{self.room_name}'

        # Garee keessa seenuu
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # NAMNI TOKKO SEENUU ISAA HUNDAAF BEEKSIISUU (ONLINE STATUS)
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'username': self.scope["user"].username,
                    'status': 'online'
                }
            )

    async def disconnect(self, close_code):
        # NAMNI TOKKO BA'UU ISAA BEEKSIISUU (OFFLINE STATUS)
        if self.scope["user"].is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'username': self.scope["user"].username,
                    'status': 'offline'
                }
            )
        
        # Garee keessaa ba'uu
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        # 1. TYPING INDICATOR HANDLER
        if data.get('type') == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_typing',
                    'username': self.scope["user"].username,
                    'typing': data.get('typing')
                }
            )
            return

        # 2. MESSAGE HANDLER
        message = data.get('message', '')
        user = self.scope["user"]
        username = user.username if user.is_authenticated else "Anonymous"
        
        image_url = data.get('image', data.get('image_url'))
        audio_url = data.get('audio', data.get('audio_url'))

        # Database-tti guduunfuu
        await self.save_message(user, message, image_url, audio_url)

        # Hundaaf Broadcast gochuu
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'image': image_url,
                'audio': audio_url,
            }
        )

    # Ergaa idilee (Message)
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event.get('message'),
            'username': event.get('username'),
            'image': event.get('image'),
            'audio': event.get('audio'),
        }))

    # Mallattoo Typing
    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'username': event['username'],
            'typing': event['typing']
        }))

    # Mallattoo Online/Offline
    async def user_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status',
            'username': event['username'],
            'status': event['status']
        }))

    @database_sync_to_async
    def save_message(self, user, message, image_url, audio_url):
        if user.is_authenticated:
            img_path = image_url.replace('/media/', '') if image_url else None
            aud_path = audio_url.replace('/media/', '') if audio_url else None
            
            Message.objects.create(
                user=user, 
                room_name=self.room_name, 
                content=message,
                image=img_path,
                audio=aud_path
            )