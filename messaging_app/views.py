from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # models.Q fayyadamuuf kana dabaladhu
from .models import Message

@login_required
def user_list(request):
    """Namoota biroo hunda (ofii kee malee) tarreessuuf"""
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/user_list.html', {'users': users})

@login_required
def chat_room(request, username):
    """Nama tokko waliin Chat gochuuf"""
    # Nama haasofsiisnu (receiver) username isaatiin barbaaduu
    other_user = get_object_or_404(User, username=username)
    
    # Ergaa gidduu isaanii jiru hunda dubbisuu
    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver=other_user)) |
        (Q(sender=other_user) & Q(receiver=request.user))
    ).order_by('timestamp')
    
    # MUUMMICH: Variable-oota asii gadii xiyyeeffannaan ilaali
    return render(request, 'chat/room.html', {
        'other_user': other_user,        # JavaScript keessatti {{ other_user.id }} ta'a
        'messages': messages,
        'other_user_id': other_user.id   # JavaScript keessatti {{ other_user_id }} ta'a
    })