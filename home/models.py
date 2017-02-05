from django.db import models
from django.core.urlresolvers import reverse


class UserInfo(models.Model):
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    reg = models.CharField(max_length=12)
    session = models.CharField(max_length=20)
    service = models.CharField(max_length=200)
    add = models.CharField(max_length=500)
    phn = models.CharField(max_length=100)


class About(models.Model):
    image_url = models.FileField()
    description = models.TextField(max_length=2000)

    def get_absolute_url(self):
        return reverse('home:index')


class Recent(models.Model):
    title = models.CharField(max_length=500)
    date = models.CharField(max_length=30)
    description = models.TextField(max_length=2000)
    image_url = models.FileField()


class Upcoming(models.Model):
    title = models.CharField(max_length=500)
    date = models.CharField(max_length=30)
    description = models.TextField(max_length=2000)
    image_url = models.FileField()

    def get_absolute_url(self):
        return reverse('home:index')


class Gallery(models.Model):
    title = models.CharField(max_length=500)
    image_url = models.FileField()

    def __str__(self):
        return self.title


class Hall_of_fame(models.Model):
    teamname = models.CharField(max_length=100)
    member1 = models.CharField(max_length=100)
    member2 = models.CharField(max_length=100)
    member3 = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    image_url = models.FileField()