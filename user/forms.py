from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class SignupForm(UserCreationForm):
    agree = forms.BooleanField(required=True, error_messages={"required": "You must agree to the Terms and Privacy Policy."},)

    
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'email')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'birth_date', 'gender', 'address', 'citizenship' , 'bio', 'email', 'phone_number']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-4 bg-slate-50 border-none rounded-2xl'}),
            'gender': forms.Select(attrs={'class': 'w-full p-4 bg-slate-50 border-none rounded-2xl'}),
        }