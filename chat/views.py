from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.
def index(req: HttpRequest):
    return render(req, "chat/index.html")

def room(req: HttpRequest, room_name: str):
    return render(req, "chat/room.html", {"room_name": room_name})
