from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.views import generic
from django.views.generic import View
from .forms import UserForm,LoginForm
from .models import Gallery,About,Recent,Upcoming,UserInfo
from django.contrib.auth.models import User


def index(request):
    all_recent = Recent.objects.all()
    all_upcoming = Upcoming.objects.all()
    all_about = About.objects.all()
    all_gallery = Gallery.objects.all()
    context = {
        'all_about':all_about,
        'all_recent':all_recent,
        'all_upcoming':all_upcoming,
        'all_gallery':all_gallery
    }
    return render(request,'home/index.html',context)


def LogOutReq(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('http://127.0.0.1:8000/home/')
    return False

def LoginFormView(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('http://127.0.0.1:8000/home/')

    return render(request, 'home/loginform.html', {'form': form})



class UserFormView(View):
    form_class = UserForm
    template_name = 'home/regform.html'

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
            userinfo = UserInfo.objects.create(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                name = form.cleaned_data['name'],
                reg = form.cleaned_data['reg'],
                session = form.cleaned_data['session'],
                service = form.cleaned_data['service'],
                add = form.cleaned_data['add'],
                phn = form.cleaned_data['phn'],
            )
            userinfo.save()

            user = authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('http://127.0.0.1:8000/home/')

        return render(request, self.template_name, {'form': form})