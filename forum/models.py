import markdown
from hashlib import md5
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

def string_color(string):
    background = int(md5(string.encode()).hexdigest(), 16) % 2**24
    tmp = background
    background = "#%06x" % background

    blue = tmp % 256
    tmp >>= 8
    green = tmp % 256
    tmp >>= 8
    red = tmp % 256

    color = "#ffffff"
    if red + green + blue > 384:
        color = "#000000"
    return (background, color)



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
            ps.add((m.author.username,) + string_color(m.author.username))
        return ps

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    text = models.TextField()
    time = models.DateTimeField('date created', auto_now_add=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def preview(self):
        return '{}...'.format(self.text[:15])

    def html(self):
        return markdown.markdown(self.text)

    def author_color(self):
        return string_color(self.author.username)

    def remove(self):
        self.deleted = True
        return self

    def restore(self):
        self.deleted = False
        return self
