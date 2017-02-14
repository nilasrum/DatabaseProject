from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Notification(models.Model):
    title = models.CharField(max_length=256)
    #message = models.TextField()
    viewed = models.BooleanField(default=False)
    approved  = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.id)+' '+str(self.user.id)


@receiver(post_save,sender=User)
def create_admin_message(sender,**kwargs):
    user = kwargs.get('instance')
    if not user.is_superuser:
        if kwargs.get('created',False):
            Notification.objects.create(user=kwargs.get('instance'),title = "new registrationn request",viewed=False)



