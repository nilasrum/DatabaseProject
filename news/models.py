from django.db import models
from django.shortcuts import render, redirect, reverse
import datetime

# Create your models here.


def curr_time():
    now = str(datetime.datetime.now())
    now = now[:16]
    return now


class AdminPost(models.Model):
    date = models.CharField(max_length=100, default=curr_time())
    post = models.TextField(max_length=1000)

    def get_absolute_url(self):
        return reverse('news:news-page')


class Contest(models.Model):
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True)
    url = models.CharField(max_length=200)
    date = models.CharField(max_length=20, blank=True)
    time = models.CharField(max_length=20, blank=True)
    duration = models.IntegerField(default=5, blank=True)

    def get_absolute_url(self):
        return reverse('news:contest-page')


class Teams(models.Model):
    name = models.CharField(max_length=100)
    member1 = models.CharField(max_length=200)
    member2 = models.CharField(max_length=200)
    member3 = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('news:teams-page')
