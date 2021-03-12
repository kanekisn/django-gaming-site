from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import *
from PIL import Image

class LoginForm(forms.Form):
    username = forms.CharField(label='Login', min_length=4, max_length=150, widget=forms.TextInput(attrs={'class' : 'validate'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class' : 'validate'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

class RegisterForm(UserCreationForm):
    username = forms.CharField(min_length = 4)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username' : forms.TextInput(attrs={'class' : 'validate'}),
            'email' : forms.EmailInput(attrs={'class' : 'validate'}),
            'password1' : forms.PasswordInput(attrs={'class' : 'validate'}),
            'password2' : forms.PasswordInput(attrs={'class' : 'validate'})
        }

class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(required=False,widget=forms.HiddenInput())
    y = forms.FloatField(required=False,widget=forms.HiddenInput())
    width = forms.FloatField(required=False,widget=forms.HiddenInput())
    height = forms.FloatField(required=False,widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ['img', 'location', 'birthdate', 'x', 'y', 'width', 'height']

        widgets = {
            'location': forms.TextInput(attrs={'class' : 'validate'}),
            'birthdate': forms.DateInput(attrs={'class' : 'datepicker'})
        }

def resizing(img, *args):
    print("я тут")
    with Image.open(img) as image:
        cropped_image = image.crop((args[0], args[1], args[2]+args[0], args[3]+args[1]))
        resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
        resized_image.save(img.path)
