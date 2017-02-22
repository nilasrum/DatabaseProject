from django.conf.urls import url
from . import views

app_name = 'news'

urlpatterns = [
    #url(r'^show/(?P<id>[0-9]+)/$',views.show_notification,name='show-notification' ),
    url(r'^list/$', views.news_page, name='news-page'),
    url(r'^list/add/$', views.CreateAdminPost.as_view(), name='add-admin-post'),
    url(r'^list/edit/(?P<pk>[0-9]+)/$',
        views.UpdateAdminPost.as_view(), name='edit-admin-post'),
    url(r'^list/delete/(?P<pk>[0-9]+)/$',
        views.DeleteAdminPost.as_view(), name='delete-admin-post'),

    url(r'^contests/$',
        views.contest_page, name='contest-page'),
    url(r'^contests/add/$', views.CreateContest.as_view(), name='add-contest'),
    url(r'^contests/edit/(?P<pk>[0-9]+)/$',
        views.UpdateContest.as_view(), name='edit-contest'),
    url(r'^contests/delete/(?P<pk>[0-9]+)/$',
        views.DeleteContest.as_view(), name='delete-contest'),

    url(r'^teams/$',
        views.team_list, name='teams-page'),
    url(r'^teams/add/$', views.CreateTeam.as_view(), name='add-team'),
    url(r'^teams/edit/(?P<pk>[0-9]+)/$',
        views.UpdateTeam.as_view(), name='edit-team'),
    url(r'^teams/delete/(?P<pk>[0-9]+)/$',
        views.DeleteTeam.as_view(), name='delete-team'),
]
