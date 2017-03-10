from django import forms
from .models import StudentProfile, OnlineContestProfile, Bio
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['name', 'reg', 'session', 'status']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class BioForm(forms.Form):

    class Meta:
        model = Bio
        fields = ['current_add', 'permanent_add', 'phone', 'about', 'working']


class CombinedFormBase(forms.Form):
    form_classes = []

    def __init__(self, *args, **kwargs):
        super(CombinedFormBase, self).__init__(*args, **kwargs)
        for f in self.form_classes:
            name = f.__name__.lower()
            setattr(self, name, f(*args, **kwargs))
            form = getattr(self, name)
            self.fields.update(form.fields)
            self.initial.update(form.initial)

    def is_valid(self):
        isValid = True
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            if not form.is_valid():
                isValid = False
        # is_valid will trigger clean method
        # so it should be called after all other forms is_valid are called
        # otherwise clean_data will be empty
        if not super(CombinedFormBase, self).is_valid():
            isValid = False
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            self.errors.update(form.errors)
        return isValid

    def clean(self):
        cleaned_data = super(CombinedFormBase, self).clean()
        for f in self.form_classes:
            name = f.__name__.lower()
            form = getattr(self, name)
            cleaned_data.update(form.cleaned_data)
        return cleaned_data


class RegistrationForm(CombinedFormBase):
    form_classes = [UserForm, StudentProfileForm]


class ProfileFormSt(forms.Form):
    name = forms.CharField(required=True)
    reg = forms.CharField(required=True)
    session = forms.CharField(required=True)
    status = forms.BooleanField(required=False)
    current_add = forms.CharField(widget=forms.Textarea, required=False)
    permanent_add = forms.CharField(widget=forms.Textarea, required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)
    phone = forms.CharField(required=False)
    working = forms.CharField(required=False)
    image_url = forms.FileField(required=False)
