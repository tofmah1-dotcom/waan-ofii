from django.contrib import admin
from .models import Post, PostImage, Comment, Category

# 1. Suuraalee baay'ee Post tokko jalatti galchuuf
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3 # Iddoo suuraa 3 qopheessi

# 2. Gosa Oduu (Category) Admin irratti galmeessuuf
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)} # Name yoo barreessitu slug ofumaan guuta

# 3. Post (Oduu) to'achuuf
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]
    # 'category' asitti dabalameera akka list irratti mul'atuuf
    list_display = ['title', 'author', 'category', 'created_at']
    
    # Title yoo barreessitu slug ofumaan akka guutuuf
    prepopulated_fields = {'slug': ('title',)} 
    search_fields = ('title', 'content')
    
    # Filter irratti 'category' dabalameera
    list_filter = ('category', 'created_at', 'author')

# 4. Yaada namootaa (Comment) galmeessuuf
admin.site.register(Comment)