import simplejson as simplejson
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Room, SeatInfo
from .forms import RoomForm
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
import logging
import json
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt


def room_region(request,region):
    rooms_contact = Room.objects.filter(name__contains=region,contact=True).order_by('created_date')
    rooms_non_contact = Room.objects.filter(name__contains=region,contact=False).order_by('created_date')

    cnt_contact = len(rooms_contact)
    cnt_non_contact = len(rooms_non_contact)
    cnt_all = cnt_contact + cnt_non_contact

    contact=[]
    for room in rooms_contact:
        cnt_empty = 0
        seatInfos = room.seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
        if len(seatInfos) >0:
            seatInfo = seatInfos[0]
            seat_data = seatInfo.data
            cnt_empty = json.loads(seat_data)['empty_seats']
        # seat_data = json.dumps(seat_data, ensure_ascii=False)
        content_contact = {'name': room.name,
                           'address': room.address,
                           'latitude': room.latitude,
                           'longitude': room.longitude,
                           'contact': room.contact,
                           'notice': room.notice,
                           'spec': room.spec,
                           'cnt_empty': cnt_empty,
                           }

        contact.append(content_contact)
        content_contact={}

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
          'contact_non':contact_non
        }


    # if not json shape, set safe parameter False
    # if contain korean, set ensure_ascil: False
    return JsonResponse(res,safe=False,json_dumps_params = {'ensure_ascii': False})

    return


@csrf_exempt
def seatInfo_save(request):
    # data = json.loads(request)

    if request.method == 'POST':
        data = request.POST.get("data")
        pcName = request.POST.get("pc_room")
        file = request.FILES['seat_image']

        room = Room.objects.filter(name__contains=pcName)
        seatInfo = SeatInfo(room=room[0],data=data,seatImage=file)
        seatInfo.save()
        return JsonResponse(json.dumps(res, ensure_ascii=False),safe=False)

def room_test(request):
    rooms_contact = Room.objects.filter(contact=True).order_by('created_date')
    rooms_non_contact = Room.objects.filter(contact=False).order_by('created_date')

    cnt_contact = len(rooms_contact)
    cnt_non_contact = len(rooms_non_contact)
    cnt_all = cnt_contact + cnt_non_contact

    contact = []
    for room in rooms_contact:
        cnt_empty = 0
        seatInfos = room.seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
        if len(seatInfos) >0:
            seatInfo = seatInfos[0]
            seat_data = seatInfo.data
            cnt_empty = json.loads(seat_data)['empty_seats']
        # seat_data = json.dumps(seat_data, ensure_ascii=False)
        content_contact = {'name': room.name,
                           'address': room.address,
                           'latitude': room.latitude,
                           'longitude': room.longitude,
                           'contact': room.contact,
                           'notice': room.notice,
                           'spec': room.spec,
                           'cnt_empty': cnt_empty,
                           }

        contact.append(content_contact)

    res = {'contact': contact}
    return JsonResponse(res, safe=False,json_dumps_params = {'ensure_ascii': False})

def room_all(request):
    rooms_contact = Room.objects.filter(contact=True).order_by('created_date')
    rooms_non_contact = Room.objects.filter(contact=False).order_by('created_date')

    cnt_contact = len(rooms_contact)
    cnt_non_contact = len(rooms_non_contact)
    cnt_all = cnt_contact + cnt_non_contact

    contact=[]
    for room in rooms_contact:
        cnt_empty = 0
        seatInfos = room.seatinfo_set.filter(created_date__lt=timezone.now()).order_by('-created_date')
        if len(seatInfos) >0:
            seatInfo = seatInfos[0]
            seat_data = seatInfo.data
            cnt_empty = json.loads(seat_data)['empty_seats']
        # seat_data = json.dumps(seat_data, ensure_ascii=False)
        content_contact = {'name': room.name,
                           'address': room.address,
                           'latitude': room.latitude,
                           'longitude': room.longitude,
                           'contact': room.contact,
                           'notice': room.notice,
                           'spec': room.spec,
                           'cnt_empty': cnt_empty,
                           }

        contact.append(content_contact)
        content_contact={}

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
          'contact_non':contact_non
        }


    # if not json shape, set safe parameter False
    # if contain korean, set ensure_ascil: False
    return JsonResponse(res,safe=False,json_dumps_params = {'ensure_ascii': False})

def room_list(request):
    rooms = Room.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'watcher/room_list.html', {'rooms':rooms})



def post_draft_list(request):
    posts = Room.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})



def room_detail(request, address):
    room = get_object_or_404(Room, address=address)
    return render(request, 'watcher/room_detail.html', {'room':room})

@login_required
def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            # room.created_date = timezone.now()
            room.save()
            return redirect('room_detail', address=room.address)
    else:
        form = RoomForm()

    return render(request, 'watcher/room_edit.html',{'form':form})

@login_required
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