from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name','employee_side', 'phone_number', 'address', 'hire_date', 'employment_status', 'num_children']
    
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
