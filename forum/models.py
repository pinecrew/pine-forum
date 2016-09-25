import markdown
from hashlib import md5
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

def string_color(string):
    return "#%06x" % (int(md5(string.encode()).hexdigest(), 16) % 2**24)

class Thread(models.Model):
    title = models.CharField(max_length=256)

    def topic(self):
        return Message.objects.filter(thread__exact=self).earliest('time')

    def last(self):
        return Message.objects.filter(thread__exact=self).latest('time')

    def messages(self):
        return Message.objects.filter(thread__exact=self).order_by('time')

    def count(self):
        return self.messages().count()

    def participants(self):
        ps = set()
        for m in self.messages():
            ps.add((m.author.username, string_color(m.author.username)))
        return ps

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

    def author_color(self):
        return string_color(self.author.username)

