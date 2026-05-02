from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Maqaa app keetii mirkaneessuuf
app_name = 'chat'

# API Router qopheessuu
router = DefaultRouter()
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    # 1. Fuula Gurguddoo (Lobby)
    path('', views.lobby, name='lobby'),
    path('search/', views.search_view, name='search'),
    path('notifications/', views.notifications_view, name='notifications'),
    
    # 2. AI Chatbot (Bakka kana murteessaadha!)
    path('ai-chat/', views.chat_view, name='chat_view'), 
    
    # 3. Chat Logic (Private & Group)
    path('start-private-chat/<int:person_id>/', views.start_private_chat, name='start_private_chat'),
    path('create-group/', views.create_group, name='create_group'),
    path('group/<int:group_id>/', views.group_room, name='group_room'),
    path('group/<int:group_id>/add-member/', views.add_member, name='add_member'),
    
    # 4. Multimedia & Actions
    path('upload_media/<int:group_id>/', views.upload_media, name='upload_media_group'),
    path('upload_media/', views.upload_media, name='upload_media_private'),
    path('delete_message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('edit_message/<int:message_id>/', views.edit_message, name='edit_message'),
    
    # 5. API URLs
    path('api/', include(router.urls)),
    
    # 6. Private Room (Yeroo hunda dhumarratti dhiisi)
    path('<str:room_name>/', views.room, name='room'),
]