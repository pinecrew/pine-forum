from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import Thread, Message

# Create your views here.
def index(request):
    threads = sorted(Thread.objects.all(), key=lambda t: t.last().time, reverse=True);
    return render(request, 'index.html', {'threads': threads})

def thread(request, thread_id):
    t = Thread.objects.get(id=thread_id)
    return render(request, 'thread.html', {'thread': t})

def message(request, thread_id, message_id):
    m = Message.objects.get(id=message_id)
    t = Thread.objects.get(id=thread_id)
    return render(request, 'post.html', {'message': m, 'thread': t})

def login(request):
    if request.user.is_authenticated():
        pass # already logged in
    else:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
        else:
            pass # go away!
    
    return redirect(request.POST['next'])
    
def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
    else:
        pass # there's no user here
    return redirect('/')
    
def new_message(request):
    
    m = Message(author=request.user,
                text=request.POST['message_text'],
                thread=request.thread)
    m.save()
    return redirect(request.POST['next'])
