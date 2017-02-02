from django.contrib.auth.models import User
from django import forms
from .models import UserInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserInfo
        fields = ['username','email','password','reg','session','name','service','add','phn']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
