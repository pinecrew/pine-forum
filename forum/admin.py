from django.contrib import admin
from .models import Message, Thread


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'get_preview', 'thread_title', 'time')

    def thread_title(self, instance):
        return instance.thread.title

    def get_preview(self, instance):
        if len(instance.text) > 18:
            return f'{instance.text[:15]}...'
        return instance.text


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title',)
