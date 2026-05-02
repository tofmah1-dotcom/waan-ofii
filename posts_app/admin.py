from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# Post Admin - Smart & Professional
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 'image_preview' fi 'total_likes_display' bakka tokkotti walitti fiduu qabna
    list_display = ('image_preview', 'title', 'author', 'category', 'total_likes_display', 'created_at')
    
    # Title yommuu barreessitu ofumaan Slug (link) uuma
    prepopulated_fields = {'slug': ('title',)}
    
    # Filter fi Search bar
    list_filter = ('category', 'created_at', 'author')
    search_fields = ('title', 'content')
    
    # Akka Post-oota baay'ee keessaa salphaatti argattuuf
    date_hierarchy = 'created_at'

    # 1. SMART PREVIEW: Suuraa Admin irratti agarsiisuuf
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 5px; object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Photo'

    # 2. SMART LIKES: Like meeqa akka qabu agarsiisuuf
    def total_likes_display(self, obj):
        return obj.total_likes()
    total_likes_display.short_description = 'Likes'