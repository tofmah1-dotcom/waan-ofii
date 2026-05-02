from django.db import models
from django.contrib.auth.models import User
import os

# --- 1. PRIVATE MESSAGE MODEL ---
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    room_name = models.CharField(max_length=255, db_index=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    audio = models.FileField(upload_to='chat_audio/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} -> {self.receiver.username if self.receiver else "Room"}: {self.content[:20]}'

    class Meta:
        ordering = ['timestamp']

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        if self.audio and os.path.isfile(self.audio.path):
            os.remove(self.audio.path)
        super().delete(*args, **kwargs)

# --- 2. CHAT GROUP MODEL ---
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True)
    group_icon = models.ImageField(upload_to='group_icons/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_groups')
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name

# --- 3. GROUP MESSAGE MODEL ---
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='group_messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)
    audio = models.FileField(upload_to='group_audio/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.user.username} @ {self.group.group_name}'

    def delete(self, *args, **kwargs):
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        if self.audio and os.path.isfile(self.audio.path):
            os.remove(self.audio.path)
        super().delete(*args, **kwargs)

# --- 4. NOTIFICATION MODEL (Amma sirriitti gadi ba'ee barreeffame) ---
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True)
    group_message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"