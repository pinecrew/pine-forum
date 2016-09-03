from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, Thread

# Create your views here.
def index(request):
    threads = Thread.objects.all()
    return render(request, 'index.html', {'threads': threads})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

