from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

from .models import Thread, Message

# Create your views here.
def index(request):
    threads = sorted(Thread.objects.all(), key=lambda t: t.last().time, reverse=True);
    return render(request, 'index.html', {'threads': threads})

def thread(request, thread_id):
    t = Thread.objects.get(id=thread_id)
    return render(request, 'thread.html', {'thread': t})

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

@csrf_exempt
def message(request, message_id):
    m = Message.objects.get(id=message_id)
    if request.method == 'GET':
        return HttpResponse(m.text, 'text/plain')
    elif request.method == 'POST':
        return redirect('/')
        m.text = request.POST['message_text']
        m.save()
        return HttpResponse(m.html(), 'text/html')

    return HttpResponse('', 'text/plain')

def new_message(request, thread_id):
    t = Thread.objects.get(id=thread_id)
    m = Message(author=request.user,
                text=request.POST['message_text'],
                thread=t)
    m.save()
    return redirect(request.POST['next'])

def del_message(request, message_id):
    m = Message.objects.get(id=message_id)
    m.remove()
    m.save()
    return redirect(request.POST['next'])

def res_message(request, message_id):
    m = Message.objects.get(id=message_id)
    m.restore()
    m.save()
    return redirect(request.POST['next'])

def edit_message(request, message_id):
    m = Message.objects.get(id=message_id)
    m.text = request.POST['message_text']
    m.save()
    return redirect(request.POST['next'])

def new_thread(request):
    t = Thread(title=request.POST['thread_title'])
    t.save()
    m = Message(author=request.user,
               text=request.POST['message_text'],
               thread=t)
    m.save()
    return redirect(request.POST['next'])
