from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Room
from .forms import RoomForm
from django.shortcuts import redirect

def room_list(request):
    rooms = Room.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'watcher/room_list.html', {'rooms':rooms})


def room_detail(request, address):
    room = get_object_or_404(Room, address=address)
    return render(request, 'watcher/room_detail.html', {'room':room})


def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_date = timezone.now()
            room.save()
            return redirect('room_detail', address=room.address)
    else:
        form = RoomForm()

    return render(request, 'watcher/room_edit.html',{'form':form})


def room_edit(request, address):
    room = get_object_or_404(Room, address=address)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_date = timezone.now()
            room.save()
            return redirect('room_detail', address=room.address)
    else:
        form = RoomForm(instance=room)
    return render(request, 'watcher/room_edit.html', {'form': form})