import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# 1. Gosa Oduu (Fkn: Ispoortii, Teknoolojii)
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 2. Barreeffama Oduu (Post)
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    
    voice_audio = models.FileField(upload_to='blog_voices/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Namoota Like godhan hunda kuusuuf
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    # OFUMAAN SLUG UUMUU: Dogoggora 'Unique' ittisuuf UUID itti dabalna
    def save(self, *args, **kwargs):
        if not self.slug:
            # Fakeenya: 'oduu-haaraa-a1b2c3d4' ta'a
            original_slug = slugify(self.title)
            self.slug = f"{original_slug}-{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)

    # Like meeqa akka qabu lakkaauuf
    def total_likes(self):
        return self.likes.count()

# 3. Suuraaleef (Multiple Images)
class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')

    def __str__(self):
        return f"Image for {self.post.title}"

# 4. Yaadaaf (Comments)
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"