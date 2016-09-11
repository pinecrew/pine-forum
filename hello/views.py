from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from .models import Thread, Message

# Create your views here.
def index(request):
    threads = sorted(Thread.objects.all(), key=lambda t: t.last().time, reverse=True);
    return render(request, 'index.html', {'threads': threads})

def thread(request, thread_id):
    t = Thread.objects.get(id=thread_id)
    return render(request, 'thread.html', {'messages': t.messages(), 'title': t.title})

def message(request, thread_id, message_id):
    m = Message.objects.get(id=message_id)
    t = Thread.objects.get(id=thread_id)
    return render(request, 'post.html', {'message': m, 'thread': t})

def login(request):
    if request.user.is_authenticated():
        pass
    else:
        username = request.POST['username']
        password = request.POST['password']

        user_list = get_user_model.objects.filter(username__exact=username)

        if user_list:
            if check_password(password, user_list[0].password):
                request.session.user = user_list[0]
        else:
            pass
