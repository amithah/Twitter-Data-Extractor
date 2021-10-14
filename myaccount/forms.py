from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(help_text="test_user")
    password = forms.CharField(widget=forms.PasswordInput,placeholder="1234@abc")
    remember_me = forms.BooleanField(required=False)


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password1', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
