from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- KUTAA 1: MODEL ERGAA (MESSAGE) ---
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    # Ergaa suuraan erguuf (Step itti aanuuf nu gargaara)
    image = models.ImageField(upload_to='chat_images/', blank=True, null=True) 
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp'] # Chat keessatti tartiiba barreeffamaatiin akka dhufuluuf

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"


# --- KUTAA 2: MODEL PROFILE NAMA (USER PROFILE) ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# --- KUTAA 3: SIGNALS (User uumamuun Profile uuma) ---
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()