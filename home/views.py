from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm, LoginForm, StudentProfileForm, RegistrationForm, ProfileFormSt
from .models import Gallery, About, Recent, Upcoming, HallOfFame, StudentProfile, ActivationStatus, OnlineContestProfile, SustContestProfile, Bio
from notification.models import Notification
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
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required

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


# test------------------------------------------------

@login_required
def member_profile_view_st(request, id):
    user = User.objects.get(id=id)
    if not ActivationStatus.objects.get(user=user).status:
        raise Http404('user is not active or does not exist')

    class FullMemberProfile(object):
        pass
    x = FullMemberProfile()
    x.id = id
    x.email = user.email
    x.username = user.username
    # print req.user.username, req.user.email
    x.name = StudentProfile.objects.get(user=user).name
    x.reg = StudentProfile.objects.get(user=user).reg
    x.session = StudentProfile.objects.get(user=user).session
    x.current_add = Bio.objects.get(user=user).current_add
    x.permanent_add = Bio.objects.get(user=user).permanent_add
    x.about = Bio.objects.get(user=user).about
    x.working = Bio.objects.get(user=user).working
    x.phone = Bio.objects.get(user=user).phone

    return render(request, 'home/member_profile_st.html', {'user': x})


def member_profile_view_oc(request, id):
    user = User.objects.get(id=id)
    if not ActivationStatus.objects.get(user=user).status:
        raise Http404('user is not active or does not exist')

    class FullMemberProfile(object):
        pass
    x = FullMemberProfile()
    x.id = OnlineContestProfile.objects.get(user=user).id
    x.rid = id
    x.name = StudentProfile.objects.get(user=user).name
    x.codeforces = OnlineContestProfile.objects.get(user=user).codeforces
    x.topcode = OnlineContestProfile.objects.get(user=user).topcode
    x.uva = OnlineContestProfile.objects.get(user=user).uva
    x.hackerrank = OnlineContestProfile.objects.get(user=user).hackerrank

    return render(request, 'home/member_profile_oc.html', {'user': x})


@cbv_decorator(login_required)
class UpdateProfileStView(FormView):
    template_name = "home/member_st_form.html"
    form_class = ProfileFormSt

    def get(self, request, id):
        user = User.objects.get(id=self.kwargs['id'])
        profile = StudentProfile.objects.get(user=user)
        bio = Bio.objects.get(user=user)
        form = self.form_class()
        context = {
            'form': form,
            'name': profile.name,
            'reg': profile.reg,
            'session': profile.session,
            'status': profile.status,
            'current_add': bio.current_add,
            'permanent_add': bio.permanent_add,
            'about': bio.about,
            'phone': bio.phone,
            'working': bio.working,
        }
        return render(request, self.template_name, context)

    def post(self, request, id):
        user = User.objects.get(id=self.kwargs['id'])
        form = self.form_class(request.POST)
        profile = StudentProfile.objects.get(user=user)
        bio = Bio.objects.get(user=user)
        profile.name = form.data['name']
        profile.reg = form.data['reg']
        profile.session = form.data['session']
        if request.POST.get('status'):
            profile.status = True
            print profile.status
        else:
            profile.status = False
        # print form.data['status'] + 'aaaaaaaaaaaaaaaaa'
        bio.current_add = form.data['current_add']
        bio.permanent_add = form.data['permanent_add']
        bio.about = form.data['about']
        bio.phone = form.data['phone']
        bio.working = form.data['working']
        profile.save()
        bio.save()
        return redirect('home:member-profile-st', id)

        return render(request, self.template_name, {'form': form})


class UpdateProfileOcView(UpdateView):
    model = OnlineContestProfile
    fields = ['codeforces', 'topcode', 'hackerrank', 'uva']

    def get_success_url(self):
        return reverse('home:member-profile-oc', kwargs={'id': self.object.user.id})
# home page
# ----------------------------------------------


def index(request):
    all_recent = Recent.objects.all()
    all_upcoming = Upcoming.objects.all()
    all_about = About.objects.all()
    all_gallery = Gallery.objects.all()
    all_hall = HallOfFame.objects.all()
    reqnum = Notification.objects.filter(viewed=False, approved=False).count()
    if reqnum > 0:
        context = {
            'all_about': all_about,
            'all_recent': all_recent,
            'all_upcoming': all_upcoming,
            'all_gallery': all_gallery,
            'all_hall': all_hall,
            'reqnum': reqnum
        }
    else:
        context = {
            'all_about': all_about,
            'all_recent': all_recent,
            'all_upcoming': all_upcoming,
            'all_gallery': all_gallery,
            'all_hall': all_hall,
        }
    return render(request, 'home/index.html', context)


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
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'user does not exist',
                           extra_tags='msg-err')
            return render(request, 'home/loginform.html', {'form': form})

        user = User.objects.get(username=username)
        if user.is_superuser:
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home:index')

        status = ActivationStatus.objects.get(
            user=user).status and user.check_password(password)
        if status is True:
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home:index')
        else:
            if user.check_password(password) is False:
                messages.error(request, 'password mismatch',
                               extra_tags='msg-err')
                return render(request, 'home/loginform.html')
            else:
                messages.warning(
                    request, 'account not approved yet', extra_tags='msg-alert')
                return render(request, 'home/loginform.html')

    return render(request, 'home/loginform.html', {'form': form})


# account-activation
#-----------------------------------------

@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err'))
def activate_account(request, id):
    status = ActivationStatus.objects.get(id=id)
    status.status = True
    status.save()
    notification = Notification.objects.get(user=status.user)
    notification.approved = True
    notification.viewed = True
    notification.save()
    email = status.user.email
    name = status.user.username
    send_mail(
        'Welcome To Acmlab,SUST',
        name + '\nYour account is now activated.\n Visit acm lab,SUST to check and configure your profile',
        'acmlabsust@example.com',
        [email],
        fail_silently=True,
    )
    messages.success(request, 'Account has been approved',
                     extra_tags='msg-success')
    return redirect('home:notification-list')

# registration
# ------------------------------------


class RegisterView(FormView):
    template_name = "home/regform.html"
    form_class = RegistrationForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            new_user = User.objects.create_user(username=username, email=form.cleaned_data[
                                                'email'], password=password)
            new_user.set_password(password)
            new_user.save()
            name = form.cleaned_data['name']
            reg = form.cleaned_data['reg']
            session = form.cleaned_data['session']
            status = form.cleaned_data['status']
            profile = StudentProfile.objects.create(
                user=new_user, name=name, reg=reg, session=session, status=status)
            profile.save()
            activation = ActivationStatus.objects.create(
                user=new_user, status=False)
            activation.save()
            return render(request, 'home/reg_admin_pending.html')

        return render(request, self.template_name, {'form': form})


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    user = kwargs.get('instance')
    if not user.is_superuser:
        if kwargs.get('created', False):
            OnlineContestProfile.objects.create(user=user)
            SustContestProfile.objects.create(user=user)
            Bio.objects.create(user=user)

# notification
# ------------------------------------------------


@user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err'))
def notification_list(request):
    all_req = Notification.objects.filter(viewed=False, approved=False)
    old_req = Notification.objects.filter(viewed=True, approved=False)

    class FullProfile(object):
        pass
    pro_list = []
    for req in all_req:
        x = FullProfile()
        x.mark_id = req.id
        x.id = ActivationStatus.objects.get(user=req.user).id
        x.email = req.user.email
        x.username = req.user.username
        # print req.user.username, req.user.email
        x.name = StudentProfile.objects.get(user=req.user).name
        x.reg = StudentProfile.objects.get(user=req.user).reg
        x.session = StudentProfile.objects.get(user=req.user).session
        pro_list.append(x)

    class FullProfileOld(object):
        pass
    old_pro_list = []
    for req in old_req:
        x = FullProfileOld()
        x.mark_id = req.id
        x.id = ActivationStatus.objects.get(user=req.user).id
        x.email = req.user.email
        x.username = req.user.username
        x.name = StudentProfile.objects.get(user=req.user).name
        x.reg = StudentProfile.objects.get(user=req.user).reg
        x.session = StudentProfile.objects.get(user=req.user).session
        old_pro_list.append(x)

    context = {
        'new_req': pro_list,
        'old_req': old_pro_list,
    }
    return render(request, 'home/notification_list.html', context)


# member list / profile
# -------------------------------------

def member_list(request):
    all_users = User.objects.all()
    all_member = []
    for user in all_users:
        if not user.is_superuser and ActivationStatus.objects.get(user=user).status:
            all_member.append(user)
    return render(request, 'home/member_list.html', {'all_member': all_member})


# about-section
# -------------------------------

@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateAbout(UpdateView):
    model = About
    fields = ['image_url', 'description']


# upcoming-section
# ---------------------------------------

def upcoming_detail(id):
    instance = get_object_or_404(Upcoming, id=id)
    return HttpResponse('<h2>hi there ' + instance.title + ' </h2>')


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class CreateUpcoming(CreateView):
    model = Upcoming
    fields = ['title', 'date', 'description', 'image_url']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateUpcoming(UpdateView):
    model = Upcoming
    fields = ['title', 'date', 'description', 'image_url']


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class DeleteUpcoming(DeleteView):
    model = Upcoming
    success_url = reverse_lazy('home:index')


# hall of fame
# -----------------------


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class CreateHalloffame(CreateView):
    model = HallOfFame
    fields = ['teamname', 'member1', 'member2', 'member3', 'coach',
              'participated', 'top10', 'top5', 'champion', 'description', 'image_url']

    def get_success_url(self):
        return reverse('home:detail-halloffame', kwargs={'id': self.object.id})


def halloffame_detail(request, id):
    team = get_object_or_404(HallOfFame, id=id)
    return render(request, 'home/team_detail.html', {'team': team})


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class UpdateHalloffame(UpdateView):
    model = HallOfFame
    fields = ['teamname', 'member1', 'member2', 'member3', 'coach',
              'participated', 'top10', 'top5', 'champion', 'description', 'image_url']

    def get_success_url(self):
        return reverse('home:detail-halloffame', kwargs={'id': self.object.id})


@cbv_decorator(user_passes_test(lambda u: u.is_staff, login_url=reverse_lazy('home:admin-err')))
class DeleteHalloffame(DeleteView):
    model = HallOfFame
    success_url = reverse_lazy('home:index')
