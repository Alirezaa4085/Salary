from django import forms
from datetime import date
from employee.models import Employee

#TODO thats socks

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10)
    payment_date = forms.DateField(label='Payment Date', initial=date.today, widget=forms.DateInput(attrs={'type': 'date'}))


class EmployeeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} - {obj.employee_side}"

class SalaryFilterForm(forms.Form):
    employee_id = EmployeeModelChoiceField(queryset=Employee.objects.all(), required=False, empty_label="All Employees")
    month = forms.CharField(max_length=7, required=False, help_text='Format: YYYY-MM')
    month2 = forms.CharField(max_length=7, required=False, help_text='Format: YYYY-MM')