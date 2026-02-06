import re  # KANA DABALUUN DIRQAMADHA
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

# 1. Fuula Lobby (Garee filachuuf)
@login_required
def lobby(request):
    return render(request, 'chat/lobby.html')

# 2. Fuula Chat Room (Namoota waliin haasa'uuf)
@login_required
def room(request, room_name):
    # KUN MURTEESSAADHA: Space-ii room_name keessa jiru gara sararaa (-) jijjiirra.
    # Akkasitti Consumer-riin wal simata, database keessaas ni argama.
    clean_room_name = re.sub(r'[^a-zA-Z0-9._-]', '-', room_name)
    
    # Amma 'clean_room_name' kanaan database irraa barbaadi
    messages = Message.objects.filter(room_name=clean_room_name).order_by('timestamp')
    
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })

# 3. Media Upload (Suuraa fi Audio erguuf)
@login_required
def upload_media(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        audio = request.FILES.get('audio')
        room_name = request.POST.get('room_name')
        
        # Room name qulqulleessi akka guduunfamuun dura
        clean_name = re.sub(r'[^a-zA-Z0-9._-]', '-', room_name)
        
        # User login godhe qofaaf database-tti guduunfuu
        msg = Message.objects.create(
            user=request.user,
            room_name=clean_name, # Clean name kanaan guduunfina
            image=image,
            audio=audio
        )
        
        file_url = ""
        if image:
            file_url = msg.image.url
        elif audio:
            file_url = msg.audio.url
            
        return JsonResponse({'status': 'success', 'url': file_url})
    
    return JsonResponse({'status': 'failed'}, status=400)

# 4. Message Delete & Edit
@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, user=request.user)
    msg.delete()
    return JsonResponse({'status': 'deleted'})

@login_required
def edit_message(request, message_id):
    return JsonResponse({'status': 'coming_soon'})

# 5. API ViewSet (Backend-iif)
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)