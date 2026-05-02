import re
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User  # KANA DABALUUN DIRQAMADHA
from django.db.models import Q
from rest_framework import viewsets, status, permissions

from .models import Message, ChatGroup, GroupMessage, Notification # Notification itti dabalameera
from .serializers import MessageSerializer

# 1. Lobby
@login_required
def lobby(request):
    groups = ChatGroup.objects.filter(members=request.user)
    # Beeksisa hin dubbisamne lakkaa'uuf
    unread_notifications = request.user.notifications.filter(is_read=False).count()
    return render(request, 'chat/lobby.html', {
        'groups': groups,
        'unread_notifications': unread_notifications
    })

# 2. Private Room
@login_required
def room(request, room_name):
    clean_room_name = re.sub(r'[^a-zA-Z0-9._-]', '-', room_name)
    messages = Message.objects.filter(room_name=clean_room_name).order_by('timestamp')
    return render(request, 'chat/room.html', {'room_name': room_name, 'messages': messages})

# 3. Group Room
@login_required
def group_room(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id)
    if request.user not in group.members.all():
        group.members.add(request.user)
    messages = group.group_messages.all().order_by('timestamp')
    return render(request, 'chat/group_room.html', {'group': group, 'messages': messages})

# 4. Create Group
@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('group_name')
        if name:
            if ChatGroup.objects.filter(group_name=name).exists():
                messages.error(request, f"Maqaan '{name}' duraan jira.")
                return render(request, 'chat/create_group.html')
            group = ChatGroup.objects.create(group_name=name, admin=request.user)
            group.members.add(request.user)
            return redirect('chat:group_room', group_id=group.id)
    return render(request, 'chat/create_group.html')

# 5. Multimedia Upload
@login_required
def upload_media(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        audio = request.FILES.get('audio')
        room_name = request.POST.get('room_name')
        msg = Message.objects.create(user=request.user, room_name=room_name, image=image, audio=audio)
        url = msg.image.url if image else msg.audio.url if audio else ""
        return JsonResponse({'status': 'success', 'url': url})
    return JsonResponse({'status': 'failed'}, status=400)

# 6. Delete Message
@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, user=request.user)
    msg.delete()
    return JsonResponse({'status': 'deleted'})

# 7. Edit Message
@login_required
def edit_message(request, message_id):
    if request.method == 'POST':
        new_content = request.POST.get('content')
        msg = get_object_or_404(Message, id=message_id, user=request.user)
        msg.content = new_content
        msg.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

# 8. Search View (Barbaacha)
@login_required
def search_view(request):
    query = request.GET.get('q', '')
    users = User.objects.none()
    groups = ChatGroup.objects.none()

    if query:
        users = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
        groups = ChatGroup.objects.filter(group_name__icontains=query)

    return render(request, 'chat/search_results.html', {
        'users': users,
        'groups': groups,
        'query': query
    })

# 9. Notifications View (Beeksisa)
@login_required
def notifications_view(request):
    notifs = request.user.notifications.all().order_by('-timestamp')
    # Yommuu fuula kana banu "read" akka ta'an gochuuf
    notifs.update(is_read=True)
    return render(request, 'chat/notifications.html', {'notifications': notifs})

# API
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)