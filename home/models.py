from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class StudentProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    reg = models.CharField(max_length=12)
    session = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ActivationStatus(models.Model):
    user = models.ForeignKey(User)
    status = models.BooleanField()

    def __str__(self):
        return str(self.id)+" "+self.user.username


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

    def __str__(self):
        return self.title


class Upcoming(models.Model):
    title = models.CharField(max_length=500)
    date = models.CharField(max_length=30)
    description = models.TextField(max_length=2000)
    image_url = models.FileField()

    def get_absolute_url(self):
        return reverse('home:index')

    def __str__(self):
        return self.title


class Gallery(models.Model):
    title = models.CharField(max_length=500)
    image_url = models.FileField()

    def __str__(self):
        return self.title


class HallOfFame(models.Model):
    teamname = models.CharField(max_length=100)
    member1 = models.CharField(max_length=100)
    member2 = models.CharField(max_length=100)
    member3 = models.CharField(max_length=100)
    coach = models.CharField(max_length=100)
    participated = models.IntegerField()
    top10 = models.IntegerField()
    top5 = models.IntegerField()
    champion = models.IntegerField()
    description = models.TextField(max_length=2000)
    image_url = models.FileField()

    def get_absolute_url(self):
        return reverse('home:index')

    def __str__(self):
        return self.teamname