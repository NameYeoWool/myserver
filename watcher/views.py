from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Room

def room_list(request):
    rooms = Room.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'watcher/room_list.html', {'rooms':rooms})


def room_detail(request, address):
    room = get_object_or_404(Room, address=address)
    return render(request, 'watcher/room_detail.html', {'room':room})