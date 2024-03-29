from django.shortcuts import render
from chatapp.models import Room
# Create your views here.

def index_view(request):     
    return render(request, 'chatapp/index.html',
    {
        'rooms':Room.objects.all(),
    })


def room_view(request, room_name):        
    chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(request, 'chatapp/room.html',{
        'room':chat_room,
    })