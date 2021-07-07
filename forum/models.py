from django.db import models
from django.contrib.auth import get_user_model

import markdown, re

User = get_user_model()


def get_deleted_user():
    return User.objects.get_or_create(username='deleted')[0]


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET(get_deleted_user))
    text = models.TextField()
    time = models.DateTimeField('date created', auto_now_add=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    editable = models.BooleanField(default=False)

    def get_preview(self):
        return f'{self.text[:15]}...' if len(self.text) > 18 else self.text

    def get_html(self):
        text = self.text
        mentions = set(re.findall(r'\B@.+?\b', text))
        user_names = set(User.objects.values_list('username', flat=True))
        for i in mentions:
            if (username := i[1:]) in user_names:
                text = text.replace(i, f'<a href="/user/{username}/">{i}</a>')
        return markdown.markdown(text, extensions=['markdown.extensions.extra'])

    def toggle_editable(self):
        self.editable = not self.editable
        return self

    def remove(self):
        self.deleted = True
        return self

    def restore(self):
        self.deleted = False
        return self


class Thread(models.Model):
    title = models.CharField(max_length=256)

    def get_messages(self):
        return self.message_set.filter(deleted=False).order_by('time')

    def get_topic(self):
        return self.get_messages().earliest('time')

    def get_last(self):
        return self.get_messages().latest('time')

    def count(self):
        return self.get_messages().count()

    def get_participants(self):
        return list(set(self.get_messages().values_list('author__username', flat=True)))[:4]
