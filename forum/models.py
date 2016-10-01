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
        return Message.objects.filter(thread__exact=self, deleted__exact=False).latest('time')

    def messages(self):
        return Message.objects.filter(thread__exact=self).order_by('time')

    def count(self):
        return self.messages().filter(deleted__exact=False).count()

    def participants(self):
        users = [i.author.username for i in self.messages()]
        ps = set(users)

        out = []
        for u in users:
            if u in ps:
                out.append((u,) + string_color(u))
                ps -= {u}
            if len(out) > 4 or len(ps) == 0:
                break
        return out

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user))
    text = models.TextField()
    time = models.DateTimeField('date created', auto_now_add=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)

    def preview(self):
        return '{}...'.format(self.text[:15]) if len(self.text) > 18 else self.text

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
