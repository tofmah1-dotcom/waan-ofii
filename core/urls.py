from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
# ASITTI: 'from chat import views' dabaluun si hin barbaachisu yoo karaa RedirectView deemte

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),

    # 2. Authentication (Login/Register)
    path('accounts/', include('allauth.urls')),

    # 3. App URLs
    path('chat/', include('chat.urls')), 
    path('blog/', include('blog.urls')),

    # 4. Root URL (/)
    # Gara Lobby-tti akka si geessu yoo barbaadde url='/chat/' godhi
    # Sababni isaa Lobby-n 'chat/urls.py' keessatti path('') ta'ee waan jiruuf
    path('', RedirectView.as_view(url='/chat/', permanent=True)),
]

# 5. Multimedia fi Static Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)