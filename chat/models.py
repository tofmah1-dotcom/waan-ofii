from django.db import models
from django.contrib.auth.models import User
import os

class Message(models.Model):
    # Nama ergaa erge
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    
    # room_name: Ergaan kun room kam keessatti akka ergame beekuuf
    room_name = models.CharField(max_length=255, db_index=True)
    
    # Barreeffama ergaa (Yoo suuraa qofa ergame duwwaa ta'uu danda'a)
    content = models.TextField(blank=True, null=True)
    
    # Multimedia Files
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True)
    audio = models.FileField(upload_to='chat_audio/', blank=True, null=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Admin irratti akka salphatti adda baasuuf
        return f'{self.user.username}: {self.content[:20] if self.content else "Media Content"}'

    class Meta:
        # Ergaan duratti ergame hunda duratti akka ba'uuf
        ordering = ['timestamp']

    # OPTIMIZATION: Ergaan yoo delete ta'e, file-oonni makiinaa keessaa akka badan godha
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        if self.audio:
            if os.path.isfile(self.audio.path):
                os.remove(self.audio.path)
        super().delete(*args, **kwargs)