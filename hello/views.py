from django.shortcuts import render
from django.http import HttpResponse

from .models import Thread

# Create your views here.
def index(request):
    threads = sorted(Thread.objects.all(), key=lambda t: t.last().time, reverse=True);
    return render(request, 'index.html', {'threads': threads})
