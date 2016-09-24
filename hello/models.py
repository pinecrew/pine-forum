import markdown
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

class Thread(models.Model):
    title = models.CharField(max_length=256)

    def topic(self):
        return Message.objects.filter(thread__exact=self).earliest('time')

    def last(self):
        return Message.objects.filter(thread__exact=self).latest('time')

    def messages(self):
        return Message.objects.filter(thread__exact=self).order_by('time')

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    text = models.TextField()
    time = models.DateTimeField('date created', auto_now_add=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)

    def preview(self):
        return '{}...'.format(self.text[:15])

    def html(self):
        return markdown.markdown(self.text)
