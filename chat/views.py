import re
import os
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, permissions

from .models import Message, ChatGroup, GroupMessage, Notification
from .serializers import MessageSerializer

# --- AI SETTINGS ---
HF_TOKEN = "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"
# Model kana Llama-3 irratti jijjiiri (Inni kun baay'ee saffisa qaba)
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# --- 0. AI CHATBOT VIEW (MULTILINGUAL) ---
@login_required
def chat_view(request):
    """
    AI Chatbot Waan-ofii: Afaan Oromoo, Amharic, fi English ni danda'a.
    """
    ai_response = ""
    user_query = ""
    
    if request.method == "POST":
        user_query = request.POST.get('message')
        
        if user_query:
            # AI-n akka afaan sadiin deebii kennu itti himuuf (System Prompt)
            # Mistral AI afaanota kana adda baasee ni beeka.
            instructions = (
                "You are the Waan-ofii Community AI Assistant. "
                "You must respond in the language the user uses: "
                "If user speaks Afaan Oromo, respond in Afaan Oromo. "
                "If user speaks Amharic, respond in Amharic. "
                "If user speaks English, respond in English. "
                "Be helpful, respectful, and culturally aware."
            )
            
            payload = {
                "inputs": f"System: {instructions}\nUser: {user_query}\nAI:",
                "parameters": {
                    "max_new_tokens": 500, 
                   "temperature": 0.8,
                   "top_p": 0.9,
                    "return_full_text": False
                }   
            }
            
            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload)
                if response.status_code == 200:
                    result = response.json()
                    # HuggingFace yeroo tokko tokko list deebisa
                    if isinstance(result, list):
                        ai_response = result[0].get('generated_text', "").strip()
                    else:
                        ai_response = result.get('generated_text', "").strip()
                    
                    # Yoo AI-n deebii isaa User: jedhee jalqabe qulqulleessuuf
                    ai_response = ai_response.replace("AI:", "").strip()
                else:
                    ai_response = "Gadi dhiifama, AI'n amma hojjechaa hin jiru. Maaloo hamma xiqqoo obsi."
            except Exception as e:
                ai_response = "Rakkoon qunnameera, irra deebii'ii yaali."

    return render(request, 'chat/chat_bot.html', {
        'response': ai_response,
        'query': user_query
    })

# --- 1. LOBBY ---
@login_required
def lobby(request):
    groups = ChatGroup.objects.filter(members=request.user)
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).count()
    return render(request, 'chat/lobby.html', {
        'groups': groups,
        'unread_notifications': unread_notifications
    })

# --- 2. START PRIVATE CHAT ---
@login_required
def start_private_chat(request, person_id):
    user1 = request.user
    user2 = get_object_or_404(User, id=person_id)
    users = sorted([user1.username, user2.username])
    room_name = f"direct_{users[0]}_{users[1]}"
    return redirect('chat:room', room_name=room_name)

# --- 3. PRIVATE ROOM VIEW ---
@login_required
def room(request, room_name):
    clean_room_name = re.sub(r'[^a-zA-Z0-9._-]', '', room_name)
    messages = Message.objects.filter(room_name=clean_room_name).order_by('timestamp')
    
    other_user = None
    if clean_room_name.startswith('direct_'):
        names = clean_room_name.replace('direct_', '').split('_')
        for name in names:
            if name != request.user.username:
                other_user = User.objects.filter(username=name).first()

    return render(request, 'chat/room.html', {
        'room_name': clean_room_name, 
        'messages': messages,
        'other_user': other_user
    })

# --- 4. GROUP ROOM VIEW ---
@login_required
def group_room(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    if request.user not in group.members.all():
        group.members.add(request.user)
    
    messages = group.group_messages.all().order_by('timestamp')
    
    return render(request, 'chat/group_room.html', {
        'group': group, 
        'messages': messages
    })

# --- 5. MULTIMEDIA UPLOAD ---
@csrf_exempt
@login_required
def upload_media(request, group_id=None):
    if request.method == 'POST':
        image = request.FILES.get('image')
        audio = request.FILES.get('audio')
        content = request.POST.get('message', '')
        
        if group_id:
            group = get_object_or_404(ChatGroup, id=group_id)
            msg = GroupMessage.objects.create(
                user=request.user, group=group, content=content, image=image, audio=audio
            )
            return JsonResponse({
                'status': 'success',
                'message_id': msg.id,
                'image_url': msg.image.url if msg.image else None,
                'audio_url': msg.audio.url if msg.audio else None,
                'username': request.user.username
            })
        else:
            room_name = request.POST.get('room_name')
            msg = Message.objects.create(
                user=request.user, room_name=room_name, content=content, image=image, audio=audio
            )
            return JsonResponse({
                'status': 'success',
                'url': msg.image.url if msg.image else (msg.audio.url if msg.audio else ""),
                'message_id': msg.id,
                'username': request.user.username
            })
    return JsonResponse({'status': 'failed'}, status=400)

# --- 6. CREATE GROUP & ADD MEMBER ---
@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('group_name')
        selected_users = request.POST.getlist('members')
        if name:
            if ChatGroup.objects.filter(group_name=name).exists():
                messages.error(request, f"Maqaan '{name}' duraan jira.")
            else:
                group = ChatGroup.objects.create(group_name=name, admin=request.user)
                group.members.add(request.user)
                if selected_users:
                    users_to_add = User.objects.filter(id__in=selected_users)
                    group.members.add(*users_to_add)
                return redirect('chat:group_room', group_id=group.id)
    
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/create_group.html', {'all_users': all_users})

@login_required
def add_member(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    if group.admin != request.user:
        messages.error(request, "Hayyama hin qabdu.")
        return redirect('chat:group_room', group_id=group.id)

    if request.method == 'POST':
        selected_users = request.POST.getlist('members')
        if selected_users:
            users_to_add = User.objects.filter(id__in=selected_users)
            group.members.add(*users_to_add)
            messages.success(request, "Miseensonni dabalamaniiru.")
        return redirect('chat:group_room', group_id=group.id)

    current_members = group.members.all().values_list('id', flat=True)
    non_members = User.objects.exclude(id__in=current_members)
    return render(request, 'chat/add_member.html', {'group': group, 'non_members': non_members})

# --- 7. DELETE, EDIT, SEARCH ---
@login_required
def delete_message(request, message_id):
    Message.objects.filter(id=message_id, user=request.user).delete()
    GroupMessage.objects.filter(id=message_id, user=request.user).delete()
    return JsonResponse({'status': 'deleted', 'message_id': message_id})

@login_required
def edit_message(request, message_id):
    if request.method == 'POST':
        new_content = request.POST.get('content')
        msg_p = Message.objects.filter(id=message_id, user=request.user).first()
        if msg_p:
            msg_p.content = new_content
            msg_p.save()
        msg_g = GroupMessage.objects.filter(id=message_id, user=request.user).first()
        if msg_g:
            msg_g.content = new_content
            msg_g.save()
        return JsonResponse({'status': 'success', 'content': new_content})
    return JsonResponse({'status': 'failed'}, status=400)

@login_required
def search_view(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query).exclude(id=request.user.id) if query else []
    groups = ChatGroup.objects.filter(group_name__icontains=query) if query else []
    return render(request, 'chat/search_results.html', {'users': users, 'groups': groups, 'query': query})

@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-timestamp')
    notifs.update(is_read=True)
    return render(request, 'chat/notifications.html', {'notifications': notifs})

# --- API ---
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)