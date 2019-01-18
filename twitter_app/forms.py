from django import forms
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):
    full_name = forms.CharField(label="First & Last Name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("full_name", "username", "email", "password")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["picture", "context"]
