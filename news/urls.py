from django.conf.urls import url
from . import views

app_name = 'news'

urlpatterns = [
    #url(r'^show/(?P<id>[0-9]+)/$',views.show_notification,name='show-notification' ),
    url(r'^list/$', views.news_page, name='news-page'),
]
