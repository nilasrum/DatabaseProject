from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^register/$', views.UserFormView.as_view(),name='register'),
    url(r'^login/$', views.LoginFormView, name='login'),
    url(r'^logout/$', views.LogOutReq,name='logout'),
]