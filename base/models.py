from django.db import models
from django.contrib.auth.models import User

# 1. Gosa Meeshaalee (Fkn: Mobile, Uffata, Meeshaa Manaa)
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="fa-box") # FontAwesome icon-f

    def __str__(self):
        return self.name

# 2. Meeshaalee Gurguraman (Products)
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    location = models.CharField(max_length=100) # Fkn: Harar, Finfinnee
    phone_number = models.CharField(max_length=20, help_text="Bilbila gurgurtaaf")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']