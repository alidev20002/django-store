from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'input', 'type':'password', 'placeholder':'رمز عبور'}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'input', 'type':'password', 'placeholder':'تکرار رمز عبور'}),
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': 'نام کاربری'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'type': 'email', 'placeholder': 'ایمیل'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'input', 'type': 'text', 'placeholder': 'نام کاربری'}))
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'input', 'type':'password', 'placeholder':'رمز عبور'}),
    )
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'type': 'text', 'placeholder': 'نام کاربری'}),
        }

class PayForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'family', 'email', 'address', 'postcode', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'نام', 'name': 'name', 'type': 'text'}),
            'family': forms.TextInput(attrs={'class': 'input', 'placeholder': 'نام خانوادگی', 'name': 'family', 'type': 'text'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'ایمیل', 'name': 'email', 'type': 'email'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placeholder': 'آدرس', 'name': 'address', 'type': 'text'}),
            'postcode': forms.TextInput(attrs={'class': 'input', 'placeholder': 'کد پستی', 'name': 'postcode', 'type': 'text'}),
            'phone': forms.TextInput(attrs={'class': 'input', 'placeholder': 'تلفن همراه', 'name': 'phone', 'type': 'tel'}),
        }