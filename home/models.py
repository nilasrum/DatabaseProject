from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    propic = models.FileField()
    name = models.CharField(max_length=100)
    reg = models.CharField(max_length=12)
    session = models.CharField(max_length=20)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class OnlineContestProfile(models.Model):
    """docstring for ."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    codeforces = models.CharField(max_length=100, blank=True)
    topcode = models.CharField(max_length=100, blank=True)
    uva = models.CharField(max_length=100, blank=True)
    hackerrank = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class SustContestProfile(models.Model):
    """docstring for ."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest1 = models.IntegerField(default=0)
    contest2 = models.IntegerField(default=0)
    contest3 = models.IntegerField(default=0)
    contest4 = models.IntegerField(default=0)
    contest5 = models.IntegerField(default=0)
    contest6 = models.IntegerField(default=0)
    contest7 = models.IntegerField(default=0)
    contest8 = models.IntegerField(default=0)
    contest9 = models.IntegerField(default=0)
    contest10 = models.IntegerField(default=0)
    contest11 = models.IntegerField(default=0)
    contest12 = models.IntegerField(default=0)
    contest13 = models.IntegerField(default=0)
    contest14 = models.IntegerField(default=0)
    contest15 = models.IntegerField(default=0)
    mx = models.IntegerField(default=0)
    mn = models.IntegerField(default=0)
    avg = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Bio(models.Model):
    """docstring for Bio."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_add = models.TextField(max_length=100, blank=True)
    permanent_add = models.TextField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    about = models.TextField(max_length=100, blank=True)
    working = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class ActivationStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()

    def __str__(self):
        return str(self.id) + " " + self.user.username


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

    # def get_absolute_url(self):
    #   return reverse('home:index')

    def __str__(self):
        return self.teamname


class UvaProblems(models.Model):
    title = models.CharField(max_length=100)
    problemid = models.IntegerField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.title
