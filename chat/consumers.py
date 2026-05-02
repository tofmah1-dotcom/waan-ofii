import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

# Model-oota barbaachisoo ta'an hunda asitti dabalera
from .models import Message, ChatGroup, GroupMessage, Notification

# Kutaa Profile sirreessuuf:
try:
    from accounts.models import Profile  # Migrations keessatti 'accounts' waan jedhuuf
except ImportError:
    try:
        from chat.models import Profile  # Yoo 'chat' keessa jiraate
    except ImportError:
        Profile = None # Yoo bakka tokkoyyuu hin jirre

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name')
        self.group_id = self.scope['url_route']['kwargs'].get('group_id')
        self.user = self.scope["user"]

        if self.group_id:
            self.room_group_name = f'chat_group_{self.group_id}'
        else:
            # Maqaa room qulqulleessuuf
            clean_name = re.sub(r'[^a-zA-Z0-9._-]', '', str(self.room_name))
            self.room_group_name = f'chat_{clean_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # --- ONLINE STATUS: CONNECT ---
        if self.user.is_authenticated:
            await self.update_user_status(True)
            # Miseensota hundaaf notify gochuu
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status_broadcast',
                    'username': self.user.username,
                    'status': 'online'
                }
            )

    async def disconnect(self, close_code):
        # --- ONLINE STATUS: DISCONNECT ---
        if self.user.is_authenticated:
            await self.update_user_status(False)
            # Miseensota hundaaf notify gochuu
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status_broadcast',
                    'username': self.user.username,
                    'status': 'offline'
                }
            )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action_type = data.get('type', 'chat_message') 
        user = self.scope["user"]

        # 1. Ergaa Haaraa Erguuf
        if action_type == 'chat_message':
            message = data.get('message', '')
            image = data.get('image', None)
            audio = data.get('audio', None)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message_handler',
                    'message': message,
                    'username': user.username,
                    'image': image,
                    'audio': audio,
                    'message_id': data.get('message_id', None)
                }
            )

        # 2. Ergaa Haquuf
        elif action_type == 'delete_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_message_handler',
                    'message_id': data.get('message_id')
                }
            )

        # 3. Ergaa Sirreessuuf
        elif action_type == 'edit_message':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'edit_message_handler',
                    'message_id': data.get('message_id'),
                    'message': data.get('message')
                }
            )

    # --- HANDLERS ---

    async def chat_message_handler(self, event):
        await self.send(text_data=json.dumps(event))

    async def delete_message_handler(self, event):
        await self.send(text_data=json.dumps({
            'type': 'delete_message',
            'message_id': event['message_id']
        }))

    async def edit_message_handler(self, event):
        await self.send(text_data=json.dumps({
            'type': 'edit_message',
            'message_id': event['message_id'],
            'message': event['message']
        }))

    async def user_status_broadcast(self, event):
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'username': event['username'],
            'status': event['status']
        }))

    @sync_to_async
    def update_user_status(self, is_online):
        if Profile is None:
            return
        try:
            # User profile is_online update gochuuf
            profile = Profile.objects.get(user=self.user)
            profile.is_online = is_online
            profile.save()
        except Exception as e:
            print(f"Status Update Error: {e}")