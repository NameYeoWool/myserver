import simplejson as simplejson
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Room
from .forms import RoomForm
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import logging

def room_all(request):
    rooms_contact = Room.objects.filter(contact=True).order_by('created_date')
    rooms_non_contact = Room.objects.filter(contact=False).order_by('created_date')

    cnt_contact = len(rooms_contact)
    cnt_non_contact = len(rooms_non_contact)
    cnt_all = cnt_contact + cnt_non_contact

    contact=[]
    for room in rooms_contact:
        content_contact = {'name': room.name ,
                   'address': room.address,
                   'latitude':room.latitude,
                   'longitude':room.longitude,
                   'contact':room.contact,
                   'notice':room.notice,
                   'spec':room.spec
                    }

        contact.append(content_contact)

    contact_non = []
    for room in rooms_non_contact:
        content_non_contact = {'name': room.name,
                           'address': room.address,
                           'latitude': room.latitude,
                           'longitude': room.longitude,
                           'contact': room.contact,
                           'notice': room.notice,
                           'spec': room.spec
                           }

        contact_non.append(content_non_contact)

    res= {'cnt_all':cnt_all,
          'cnt_contact':cnt_contact,
          'cnt_non_contact':cnt_non_contact,
          'contact':contact,
          'content_non':contact_non
        }


    # if not json shape, set safe parameter False
    # if contain korean, set ensure_ascil: False
    return JsonResponse(res,safe=False,json_dumps_params = {'ensure_ascii': False})

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
            room.save()
            return redirect('room_detail', address=room.address)
    else:
        form = RoomForm(instance=room)
    return render(request, 'watcher/room_edit.html', {'form': form})