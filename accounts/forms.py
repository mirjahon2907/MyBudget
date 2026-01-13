from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'email')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name","last_name", "bio", "email", "phone_number","address"]