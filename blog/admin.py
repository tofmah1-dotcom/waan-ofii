from django.contrib import admin
from .models import Post, PostImage, Comment

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3 # Iddoo suuraa 3 qopheessi

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]
    list_display = ['title', 'author', 'created_at']

admin.site.register(Comment)