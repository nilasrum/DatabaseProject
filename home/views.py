from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForm,LoginForm,StudentProfileForm,RegistrationForm
from .models import Gallery,About,Recent,Upcoming,HallOfFame,StudentProfile,ActivationStatus
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms import inlineformset_factory
from django import forms
from django.views.generic import FormView
from django.core.mail import send_mail

# self_defined useful functions
# --------------------------------------------

def admin_error(request):
    raise Http404("may be u shouldn't be here")


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


# home page
# ----------------------------------------------

def index(request):
    all_recent = Recent.objects.all()
    all_upcoming = Upcoming.objects.all()
    all_about = About.objects.all()
    all_gallery = Gallery.objects.all()
    all_hall = HallOfFame.objects.all()
    context = {
        'all_about':all_about,
        'all_recent':all_recent,
        'all_upcoming':all_upcoming,
        'all_gallery':all_gallery,
        'all_hall':all_hall
    }
    return render(request,'home/index.html',context)


# login/logout
# ------------------------------------------

def logout_req(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('home:index')
    return False


def login_form_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.get(username=username)
        if user.is_superuser:
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home:index')
        try:
            status = ActivationStatus.objects.get(user=user)
            if status.status is True:
                user = authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    return redirect('home:index')
            else:
                return render(request,'home/account_not_activated.html')
        except User.DoesNotExist:
            return render(request, 'home/loginform.html', {'form': form})

    return render(request, 'home/loginform.html', {'form': form})


@user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err'))
def activate_account(request,id):
    status = ActivationStatus.objects.get(id=id)
    status.status=True
    status.save()
    email = status.user.email
    send_mail(
        'Welcome To Acmlab,SUST',
        'Your account is now activated.\n Visit acm lab,SUST to check and configure your profile',
        'acmlabsust@example.com',
        [email],
        fail_silently=True,
    )
    name = status.user.username
    return render(request,'home/account_approved.html',{'name':name})


class RegisterView(FormView):
    template_name = "home/regform.html"
    form_class = RegistrationForm

    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            new_user = User.objects.create_user(username=username, email=form.cleaned_data['email'],password=password)
            new_user.set_password(password)
            new_user.save()
            name = form.cleaned_data['name']
            reg = form.cleaned_data['reg']
            session = form.cleaned_data['session']
            profile = StudentProfile.objects.create(user=new_user,name=name,reg=reg,session=session)
            profile.save()
            activation = ActivationStatus.objects.create(user=new_user,status=False)
            activation.save()
            return render(request,'home/reg_admin_pending.html')

        return render(request, self.template_name, {'form': form})


# about-section
# -------------------------------

@cbv_decorator(user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateAbout(UpdateView):
    model = About
    fields = ['image_url','description']


# upcoming-section
# ---------------------------------------

def upcoming_detail(requst,id):
    instance = get_object_or_404(Upcoming,id=id)
    return HttpResponse('<h2>hi there '+instance.title+' </h2>')


@cbv_decorator(user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err')))
class CreateUpcoming(CreateView):
    model = Upcoming
    fields = ['title','date','description','image_url']


@cbv_decorator(user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateUpcoming(UpdateView):
    model = Upcoming
    fields = ['title','date','description','image_url']


@cbv_decorator(user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err')))
class DeleteUpcoming(DeleteView):
    model = Upcoming
    success_url = reverse_lazy('home:index')


# hall of fame
# -----------------------


@cbv_decorator(user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err')))
class CreateHalloffame(CreateView):
    model = HallOfFame
    fields = ['teamname','member1','member2','member3','coach','top10','top5','champion','description','image_url']


def halloffame_detail(request,id):
    team = get_object_or_404(HallOfFame,id=id)
    return render(request,'home/team_detail.html',{'team':team})


@cbv_decorator(user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateHalloffame(UpdateView):
    model = HallOfFame
    fields = ['teamname','member1','member2','member3','coach','top10','top5','champion','description','image_url']


@cbv_decorator(user_passes_test(lambda u:u.is_staff, login_url=reverse_lazy('home:admin-err')))
class DeleteHalloffame(DeleteView):
    model = HallOfFame
    success_url = reverse_lazy('home:index')

