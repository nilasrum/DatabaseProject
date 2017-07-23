from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from .models import AdminPost, Contest, Teams
import datetime

# Create your views here.


def cbv_decorator(decorator):
    """
    Turns a normal view decorator into a class-based-view decorator.
    Usage:
    @cbv_decorator(login_required)
    class MyClassBasedView(View):
        pass
    """
    def _decorator(cls):
        cls.dispatch = method_decorator(decorator)(cls.dispatch)
        return cls

    return _decorator


@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('home:admin-err'))
def news_page(request):
    all_news = []
    news = AdminPost.objects.all()
    for n in news[::-1]:
        all_news.append(n)
    recent = []
    older = []
    for news in all_news[:5]:
        recent.append(news)
    for news in all_news[5:]:
        older.append(news)
    context = {
        'older': older,
        'recent': recent,
    }

    return render(request, 'news/news_page.html', context)


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class CreateAdminPost(CreateView):
    model = AdminPost
    now = str(datetime.datetime.now())
    now = now[:19]
    model.date = now
    fields = ['title','post']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateAdminPost(UpdateView):
    model = AdminPost
    fields = ['post']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class DeleteAdminPost(DeleteView):
    model = AdminPost
    success_url = reverse_lazy('news:news-page')


@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('home:admin-err'))
def contest_page(request):

    all_contest = []
    contest = Contest.objects.all()
    for c in contest[::-1]:
        all_contest.append(c)
    recent = []
    older = []
    for c in all_contest[:5]:
        recent.append(c)
    for c in all_contest[5:]:
        older.append(c)
    context = {
        'older': older,
        'recent': recent,
    }

    return render(request, 'news/contest_page.html', context)


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class CreateContest(CreateView):
    model = Contest
    fields = ['title', 'description', 'date', 'time', 'duration', 'url']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateContest(UpdateView):
    model = Contest
    fields = ['title', 'description', 'date', 'time', 'duration', 'url']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class DeleteContest(DeleteView):
    model = Contest
    success_url = reverse_lazy('news:contest-page')


@user_passes_test(lambda u: u.is_authenticated, login_url=reverse_lazy('home:admin-err'))
def team_list(request):
    all_teams = Teams.objects.all()
    return render(request, 'news/team_page.html', {'all_teams': all_teams})


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class CreateTeam(CreateView):
    model = Teams
    fields = ['name', 'member1', 'member2', 'member3']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateTeam(UpdateView):
    model = Teams
    fields = ['name', 'member1', 'member2', 'member3']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class DeleteTeam(DeleteView):
    model = Teams
    success_url = reverse_lazy('news:teams-page')
