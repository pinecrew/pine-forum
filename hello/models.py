from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Thread(models.Model):
    title = models.CharField(max_length=256)

    def topic(self):
        Message.objects.filter(thread==self).aggregate(models.Min('date'))
    def last(self):
        Message.objects.filter(thread==self).aggregate(models.Max('date'))

class Message(models.Model):
    author = models.CharField(max_length=256)
    text = models.TextField()
    time = models.DateTimeField('date created', auto_now_add=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)