from django import forms
from .models import *

class ServersAddForm(forms.ModelForm):
    class Meta:
        model = Servers
        fields = ['ip', 'port', 'password']

        widgets = {
            'ip' : forms.TextInput(attrs={'class' : 'validate'}),
            'port' : forms.NumberInput(attrs={'class' : 'validate'}),
            'password' : forms.PasswordInput(attrs={'class' : 'validate'}),
        }