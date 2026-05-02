from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views 

# 1. API ROUTER (Bilbila/Mobile-f)
router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

app_name = 'blog' 

urlpatterns = [
    # --- KAN BROWSER (Templates) ---
    path('', views.post_list, name='post_list'), 

    # 'create/' sarara 'slug' gubbaa jiraachuu qaba
    path('create/', views.post_create, name='post_create'),

    path('<slug:slug>/', views.post_detail, name='post_detail'), 
    
    # !!! KANA ITTI DABALI: Oduu haquuf
    path('<slug:slug>/delete/', views.post_delete, name='post_delete'),

    path('<slug:slug>/comment/', views.add_comment, name='add_comment'), 

    # --- KAN API (Mobile/JSON) ---
    path('api/', include(router.urls)), 
]