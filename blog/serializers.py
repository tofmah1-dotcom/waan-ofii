from rest_framework import serializers
from .models import Post, Comment, PostImage

# 1. Suuraaleef (Gallery)
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'image']

# 2. Yaadaaf (Comments)
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'author_username', 'text', 'created_at']

# 3. Barreeffamaaf (Post)
class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    images = PostImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'author', 
            'author_username', 
            'title', 
            'content', 
            'images', 
            'voice_audio', 'created_at', 
            'comments', 'category'
        ]
        # KANA DABALADHU: Author akka HTML irraa hin barbaadne godha
        read_only_fields = ['author']