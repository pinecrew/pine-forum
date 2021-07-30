import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.db.models import Max, Subquery, OuterRef
from django.utils.functional import cached_property
from django.urls import reverse, reverse_lazy

from rest_framework import mixins, viewsets, response
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_json_api.renderers import JSONRenderer

from .models import Thread, Message
from .forms import MessageForm, ThreadForm
from .serializers import MessageSerializer
from .permissions import MessagePermission
from .services.markdown import render_html


class IndexView(FormMixin, ListView):
    template_name = 'index.html'
    model = Thread
    form_class = ThreadForm

    def get_queryset(self):
        return self.model.objects.annotate(last_updated=Max('message__time')).order_by(
            '-last_updated'
        )


class ThreadDetailView(SingleObjectMixin, FormMixin, ListView):
    template_name = 'thread.html'
    form_class = MessageForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Thread.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.message_set.order_by('time')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse('thread', kwargs={'pk': self.object.thread.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.thread = Thread.objects.get(pk=self.kwargs.get('thread_id'))
        return super().form_valid(form)


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


class MessageViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (MessagePermission,)
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'message.html'

    def perform_destroy(self, instance):
        instance.remove()
        instance.save()

    def partial_update(self, request, *args, **kwargs):
        r = super().partial_update(request, *args, **kwargs)
        if request.accepted_renderer.format == 'html':
            return response.Response({'m': self.get_object})
        return r

    @action(detail=True, methods=['get'])
    def restore(self, request, pk=None):
        instance = self.get_object()
        instance.restore()
        instance.save()

        # TemplateHtmlRenderer
        if request.accepted_renderer.format == 'html':
            return response.Response({'m': instance})

        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class ThreadCreateView(CreateView):
    model = Message
    form_class = ThreadForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.thread = Thread.objects.create(title=form.cleaned_data['title'])
        return super().form_valid(form)


class ProfileView(DetailView):
    model = User
    slug_url_kwarg = 'username'
    slug_field = 'username'
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msgs = Message.objects.filter(
            author=self.object, deleted__exact=False
        ).order_by('-time')
        msgcount = msgs.count()
        trdcount = (
            Thread.objects.annotate(
                author=Subquery(
                    Message.objects.filter(thread=OuterRef('pk'))
                    .order_by('time')
                    .values('author')[:1]
                )
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
