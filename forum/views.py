import django.contrib.auth as auth
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from functools import reduce

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

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
        else:
            pass # go away!

    return redirect(request.POST['next'])

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    else:
        pass # there's no user here
    return redirect('/')

def message_new(request, thread_id):
    t = Thread.objects.get(id=thread_id)
    m = Message(author=request.user,
                text=request.POST['message_text'],
                thread=t)
    m.save()
    return redirect(request.POST['next'])

@csrf_exempt
def message(request, message_id):
    m = Message.objects.get(id=message_id)
    if request.method == 'GET':
        return HttpResponse(m.text, 'text/plain')
    elif request.method == 'POST':
        m.text = request.body.decode()
        m.save()
        return HttpResponse(m.html(), 'text/html')

    return HttpResponse('', 'text/plain')

@csrf_exempt
def message_tog(request, message_id):
    m = Message.objects.get(id=message_id)
    if request.method == 'GET':
        m.restore()
    elif request.method == 'POST':
        m.remove()
    else:
        return HttpResponse('', 'text/plain')

    m.save()
    return render(request, 'message.html', {'m': m, 'thread': m.thread})

def thread_new(request):
    t = Thread(title=request.POST['thread_title'])
    t.save()
    m = Message(author=request.user,
               text=request.POST['message_text'],
               thread=t)
    m.save()
    return redirect(request.POST['next'])

def profile(request, name):
    user = User.objects.get(username=name)
    msgcount = Message.objects.filter(author__username__exact=username).count()
    trds = filter(lambda x: x.topic().author.username == username, Thread.objects.all())
    trdcount = reduce(lambda acc, _: acc + 1, trds, 0)
    return render(request, 'profile.html', {'usr': user, 'msgcount': msgcount, 'trdcount': trdcount})

def user_new(request):
    username = request.POST['username']
    user = User.objects.create_user(username, password=username)
    user.save()
    return redirect(request.POST['next'])

def change_password(request):
    u = request.user
    u.set_password(request.POST['password'])
    u.save()
    return redirect(request.POST['next'])
