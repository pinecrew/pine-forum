from django.forms import ModelForm, CharField

from .models import Message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ('text',)


class ThreadForm(ModelForm):
    title = CharField()

    class Meta:
        model = Message
        fields = ('title', 'text')
