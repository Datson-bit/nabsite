from django import forms
from django.contrib.auth.forms import UserCreationForm 

class UserRegister(UserCreationForm):
    email = forms.EmailField()

    class meta:
        model = 'db'
        fields = ('username', 'email', 'password1', 'password2')