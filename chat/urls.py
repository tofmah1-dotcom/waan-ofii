from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', views.lobby, name='lobby'),
    path('api/', include(router.urls)),
    
    # KANA SIRREESSI: <path:room_name> jennaan / k/HR/WHR/ hunda ni fudhata
    path('<path:room_name>/', views.room, name='room'),
    
    path('upload_media/', views.upload_media, name='upload_media'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
]