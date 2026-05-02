from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    
    # --- ONLINE STATUS DABALAMEERA ---
    # Namni sun banee jiraachuu isaa mirkaneessuuf
    is_online = models.BooleanField(default=False)
    
    # Yoom akka bane beekuuf (Last Seen)
    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'

    # Namni sun yoom akka bane update gochuuf
    def update_last_seen(self):
        self.last_seen = timezone.now()
        self.save()

# --- SIGNALS (Akka koodii kee isa duraatti) ---

# User yommuu uumamu Profile akka uumamuuf
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

# Profile save gochuuf
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()