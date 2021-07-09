import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.db.models import Max, Subquery, OuterRef

from functools import reduce

from .models import Thread, Message


class IndexView(ListView):
    template_name = 'index.html'
    model = Thread

    def get_queryset(self):
        return self.model.objects.annotate(last_updated=Max('message__time')).order_by('-last_updated')


class ThreadDetailView(SingleObjectMixin, ListView):
    template_name = 'thread.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Thread.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['thread'] = self.object
        return context

    def get_queryset(self):
        return self.object.message_set.order_by('time')


def login(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            pass  # already logged in
        else:
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
            else:
                pass  # go away!
        return redirect(request.POST['next'])
    else:
        return redirect('/')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    else:
        pass  # there's no logged user here
    return redirect('/')


def message_new(request, thread_id):
    t = Thread.objects.get(id=thread_id)
    m = Message(author=request.user, text=request.POST['message_text'], thread=t)
    m.save()
    return redirect(request.POST['next'])


@csrf_exempt
def message(request, message_id):
    m = Message.objects.get(id=message_id)
    if request.method == 'GET':
        if request.user != m.author:
            editable = "Forbidden"
        else:
            editable = m.editable
        return HttpResponse([m.text, editable], 'text/plain')
    elif request.method == 'POST':
        body = request.body.decode().split(',')
        m.text, m.editable = ','.join(body[:-1]), body[-1]
        if m.editable == 'true':
            m.editable = True
        else:
            m.editable = False
        m.save()
        return HttpResponse(m.get_html(), 'text/html')

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
    m = Message(author=request.user, text=request.POST['message_text'], thread=t)
    m.save()
    return redirect(request.POST['next'])


class ProfileView(DetailView):
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs = Message.objects.filter(author=self.object, deleted__exact=False).order_by('-time')
        msgcount = msgs.count()
        trdcount = (
            Thread.objects.annotate(
                author=Subquery(Message.objects.filter(thread=OuterRef('pk')).order_by('time').values('author')[:1])
            )
            .filter(author=self.object)
            .count()
        )
        context.update({'msgs': msgs[:5], 'msgcount': msgcount, 'trdcount': trdcount})
        return context


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
