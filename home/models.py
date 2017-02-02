from django.db import models


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
    image_url = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)

    def __str__(self):
        return self.image_url


class Recent(models.Model):
    title = models.CharField(max_length=500)
    date = models.CharField(max_length=30)
    description = models.CharField(max_length=5000)
    image_url = models.CharField(max_length=1000)


class Upcoming(models.Model):
    title = models.CharField(max_length=500)
    date = models.CharField(max_length=30)
    description = models.CharField(max_length=5000)
    image_url = models.CharField(max_length=1000)


class Gallery(models.Model):
    title = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)

    def __str__(self):
        return self.title+"-"+self.image_url


class Hall_of_fame(models.Model):
    teamname = models.CharField(max_length=100)
    member1 = models.CharField(max_length=100)
    member2 = models.CharField(max_length=100)
    member3 = models.CharField(max_length=100)
    description = models.CharField(max_length=5000)