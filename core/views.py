from django.shortcuts import render
from posts_app.models import Post
from academy_app.models import Course
from django.contrib.auth.models import User # KANA ITTI DABALI

def home_view(request):
    # 1. Barreeffamoota haaraa 3 qofa fida
    recent_posts = Post.objects.all().order_by('-created_at')[:3]
    
    # 2. Koorsiiwwan haaraa 3 qofa fida
    featured_courses = Course.objects.all().order_by('-id')[:3]

    # 3. Namoota (Users) hunda fida (Chat irratti akka mul'ataniif)
    # Ofii kee akka siif hin mul'anneef .exclude(id=request.user.id) fayyadamuu dandeessa
    all_users = User.objects.all()

    # 4. Saanduqa (Context) keessatti hunda qindeessina
    context = {
        'posts': recent_posts,
        'courses': featured_courses,
        'users': all_users, # KANA ITTI DABALUUN MURTEESSAADHA
    }
    
    return render(request, 'home.html', context)