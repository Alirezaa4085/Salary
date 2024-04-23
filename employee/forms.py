from django import forms
from getsalari.models import UserProfile, Employee, Expense
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
# from django.contrib.auth.models import User
from django.utils.timezone import now, localtime
from datetime import date


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone_number', 'address', 'hire_date', 'employment_status', 'num_children']
    
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['num_children'].widget = forms.HiddenInput()

        if 'employment_status' in self.data and self.data['employment_status'] == 'True':
            self.fields['num_children'].widget = forms.NumberInput()
        self.fields['hire_date'].widget = forms.DateInput(attrs={'type': 'date'})

class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone_number', 'hire_date', 'employment_status', 'num_children', 'address']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hire_date'].widget = forms.DateInput(attrs={'type': 'date'})
