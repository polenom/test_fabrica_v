import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class OperatorCode(models.Model):
    name = models.CharField(max_length=20, help_text='operator name')
    code = models.IntegerField()

    def __str__(self):
        return self.name


class Distribution(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='distribution')
    start = models.DateTimeField(help_text='Time is starting')
    finish = models.DateTimeField(help_text='Time is finishing')
    text = models.TextField(max_length=300)
    filter_tag = models.ManyToManyField(Tag)
    filter_code = models.ManyToManyField(OperatorCode)


class Client(models.Model):
    TIMEZONE_CHOICES = zip(pytz.all_timezones, pytz.all_timezones)

    phone_number = models.CharField(max_length=12)
    code = models.ForeignKey(OperatorCode,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='clients')
    tag = models.ManyToManyField(Tag)
    timezone = models.CharField(max_length=32,
                                choices=TIMEZONE_CHOICES)


class Message(models.Model):
    class Status(models.TextChoices):
        r = 'r', 'running'
        e = 'e', 'error'
        c = 'c', 'complite'

    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1,
                              choices=Status.choices)
    distribution = models.ForeignKey(Distribution,
                                     on_delete=models.CASCADE,
                                     related_name='message')
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='message')
