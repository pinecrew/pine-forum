from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User

import markdown, re

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
        users = [i.author.username for i in self.messages() if not i.deleted]
        ps = set(users)

        out = []
        for u in users:
            if u in ps:
                out.append(u)
                ps -= {u}
            if len(out) > 4 or len(ps) == 0:
                break
        return out


class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL
                              ,on_delete=models.SET(lambda: get_user_model().objects
                                                                            .get_or_create(username='deleted')[0])
                              )
    text = models.TextField()
    time = models.DateTimeField('date created', auto_now_add=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    editable = models.BooleanField(default=False)

    def preview(self):
        return '{}...'.format(self.text[:15]) if len(self.text) > 18 else self.text

    def html(self):
        text = self.text
        mentions = set(re.findall(r'\B@.+?\b', text))
        for i in mentions:
            user = User.objects.filter(username__exact=i[1:]).first()
            if user:
                text = text.replace(i, '<a href="/user/{}/">{}</a>'.format(user.username, i))
        return markdown.markdown(text, ['markdown.extensions.extra'])

    def toggle_editable(self):
        self.editable = not self.editable
        return self

    def remove(self):
        self.deleted = True
        return self

    def restore(self):
        self.deleted = False
        return self
