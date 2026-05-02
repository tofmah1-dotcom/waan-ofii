from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.core.paginator import Paginator # Pagination'f
from .models import Post, PostImage, Comment, Category
from .serializers import PostSerializer, CommentSerializer

# ==========================================
# 1. API VIEWS (React/Frontend ykn API-f)
# ==========================================
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Data dhufu hantuutee (request.data) irraa fuuna
        data = request.data.copy() 
        images = request.FILES.getlist('uploaded_images')
        voice = request.FILES.get('voice_audio')

        serializer = self.get_serializer(data=data)
        
        # Yoo serializer-riin dogoggora qabaate terminal irratti akka arginuuf
        if not serializer.is_valid():
            print("DOGOGGORA SERIALIZER:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Author fi Voice Audio asitti save ta'a
        post_instance = serializer.save(
            author=request.user, 
            voice_audio=voice
        )

        # Suuraalee baay'ee yoo jiraatan tokko tokkoon kuusa
        for image in images:
            PostImage.objects.create(post=post_instance, image=image)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ==========================================
# 2. TEMPLATE VIEWS (Browser-irratti ilaaluuf)
# ==========================================

def post_list(request):
    # Oduu hunda fidi
    posts_list = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()

    # DEBUG: Terminal irratti oduu meeqa akka jiru siif barreessa
    print(f"DEBUG: Oduuwwan Database keessa jiran -> {posts_list.count()}")

    # Search (Barbaaduu)
    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    # Category-n adda baasuu
    category_slug = request.GET.get('category')
    if category_slug:
        posts_list = posts_list.filter(category__slug=category_slug)

    # PAGINATION: Fuula tokko irratti oduu 6 qofa agarsiisa
    paginator = Paginator(posts_list, 6) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'categories': categories,
        'search_query': query,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    images = post.images.all() 
    comments = post.comments.all().order_by('-created_at')
    
    context = {
        'post': post,
        'images': images,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_create(request):
    categories = Category.objects.all()
    return render(request, 'blog/post_create.html', {'categories': categories})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author == request.user:
        post.delete()
    return redirect('blog:post_list')

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        text = request.POST.get('text')
        if text:
            Comment.objects.create(
                post=post,
                user=request.user,
                text=text
            )
    return redirect('blog:post_detail', slug=slug)