import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class OperatorCode(models.Model):
    name = models.CharField(max_length=20, help_text='operator name')
    code = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Distribution(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='distribution')
    start = models.DateTimeField(help_text='Time is starting')
    finish = models.DateTimeField(help_text='Time is finishing')
    text = models.TextField(max_length=300)


class Client(models.Model):
    TIMEZONE_CHOICES = zip(pytz.all_timezones, pytz.all_timezones)

    phone_number = models.CharField(max_length=12, unique=True)
    code = models.ForeignKey(OperatorCode,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='clients')
    timezone = models.CharField(max_length=32,)


class TagForClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=30)

    class Meta:
        unique_together = ('client', 'name',)
    def __str__(self):
        return self.name


class FilterTag(models.Model):
    task = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='filter_tag')
    name = models.CharField(max_length=100)


class FilterCode(models.Model):
    task = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='filter_code')
    code = models.IntegerField()


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
