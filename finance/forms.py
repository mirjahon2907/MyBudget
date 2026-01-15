from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Transactions


class TransactionsAddForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('amount','category', 'wallet')
