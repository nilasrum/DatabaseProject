from django.conf.urls import url
from . import views

app_name = 'notification'

urlpatterns = [
    #url(r'^show/(?P<id>[0-9]+)/$',views.show_notification,name='show-notification' ),
    url(r'^delete/(?P<id>[0-9]+)/$',views.del_notification,name='del-notification' ),
]