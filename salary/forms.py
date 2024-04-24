from django import forms
from datetime import date


#TODO thats socks

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10, decimal_places=2)
    payment_date = forms.DateField(label='Payment Date', initial=date.today, widget=forms.DateInput(attrs={'type': 'date'}))


