from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Post, PostImage, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # 1. Data makiinaan ergame hunda fudhu
        data = request.data
        images = request.FILES.getlist('uploaded_images')
        voice = request.FILES.get('voice_audio') # Saagalee battalatti waraabame fida

        # 2. Serializer-itti kenni
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            # 3. Author fi voice_audio dabalii kuusi
            # 'serializer.save()' instance 'Post' deebisa
            post_instance = serializer.save(
                author=self.request.user, 
                voice_audio=voice
            )
            
            # 4. Suuraalee baay'ee yoo jiraatan tokko tokkoon kuusi
            for image in images:
                PostImage.objects.create(post=post_instance, image=image)
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Namni yaada kenne author yaada sanaa godhamuun galmaa'a
        serializer.save(user=self.request.user)