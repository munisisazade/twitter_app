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


class UserSettingsForm(forms.ModelForm):
    current_password = forms.CharField()
    confirm_password = forms.CharField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    def clean_confirm_password(self):
        password1 = self.cleaned_data.get("current_password")
        password2 = self.cleaned_data.get("confirm_password")
        if password1 == password2:
            pass
        else:
            raise forms.ValidationError("Password don't match")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["picture", "context"]
