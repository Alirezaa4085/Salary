from django import forms
# from .models import UserProfile, Employee, Expense
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
# from django.contrib.auth.models import User
from django.utils.timezone import now, localtime
from datetime import date


#TODO thats socks

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    payment_date = forms.DateField(label='Payment Date', initial=date.today, widget=forms.DateInput(attrs={'type': 'date'}))


