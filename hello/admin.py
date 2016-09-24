from django.contrib import admin
from .models import Message, Thread
# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'thread.title', 'time')

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title',)
