from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from models import Notification

# Create your views here.


#def show_notification(request,id):
#    #n = Notification.objects.get(pk=notification_id)
#    instance = get_object_or_404(Notification,id=id)
#    return render(request,'notification/notification.html',{'notification':instance})

@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err'))
def del_notification(request,id):
    #n = Notification.objects.get(pk=notification_id)
    instance = get_object_or_404(Notification,id=id)
    instance.viewed=True
    instance.save()
    return redirect('home:notification-list')