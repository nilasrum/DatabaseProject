from django.conf.urls import url
from .import views

app_name = 'home'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^register/$', views.UserFormView.as_view(),name='register'),
    url(r'^login/$', views.login_form_view, name='login'),
    url(r'^logout/$', views.logout_req,name='logout'),

    url(r'^upcoming/(?P<id>[0-9]+)/$', views.upcoming_detail,name='upcoming-detail'),
    url(r'^add/upcoming/$', views.CreateUpcoming.as_view(),name='add-upcoming'),
    url(r'^upcoming/(?P<pk>[0-9]+)/edit/$', views.UpdateUpcoming.as_view(),name='edit-upcoming'),
    url(r'^upcoming/(?P<pk>[0-9]+)/delete/$', views.DeleteUpcoming.as_view(),name='delete-upcoming'),

    url(r'^about/(?P<pk>[0-9]+)/edit/$', views.UpdateAbout.as_view(),name='edit-about'),
    url(r'^adminerr/$', views.admin_error,name='admin-err'),
]