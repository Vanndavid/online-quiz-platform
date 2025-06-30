from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
from django.forms import ModelForm
from django.core.validators import EmailValidator, MinLengthValidator

class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['name', 'email','role', 'password1', 'password2'] #updated by ronald - added username


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2'] #updated by ronald - added username

          
class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['name', 'email', 'role'] 

class ResetPasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['password1', 'password2'] 