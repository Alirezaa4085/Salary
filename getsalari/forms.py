from django import forms
from django.utils.timezone import now, localtime
from employee.models import Employee



class EmployeeSearchForm(forms.Form):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(), empty_label="Select an employee")


class MonthSelectForm(forms.Form):
    months_choices = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    today = localtime(now())
    current_month = today.month
    current_year = today.year
    month = forms.ChoiceField(choices=months_choices, label='Select Month', initial=current_month)
    year = forms.IntegerField(label='Year', initial=current_year, min_value=1970, max_value=2100)

    def clean_year(self):
        year = self.cleaned_data['year']
        if year == self.today.year:
            return year
        raise forms.ValidationError("You can only select the current year.")

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('month')
        year = cleaned_data.get('year')
        today = self.today
        if year == today.year and int(month) > today.month:
            raise forms.ValidationError("You can only select past months in the current year.")
        return cleaned_data
    
#######################################form login checks####################################################

# class CustomUserChangeForm(UserChangeForm):
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=30, required=False)
#     email = forms.EmailField(required=False)

#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email']

# class CustomPasswordChangeForm(PasswordChangeForm):
#     class Meta:
#         model = User



# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ['name', 'phone_number', 'hire_date', 'employment_status', 'num_children', 'address']
#     def __init__(self, *args, **kwargs):
#         super(EmployeeForm, self).__init__(*args, **kwargs)
#         self.fields['num_children'] = forms.IntegerField(
#             label='Number of Children',
#             required=False,
#             widget=forms.NumberInput(attrs={'class': 'form-control'})
#         )

#     def clean(self):
#         cleaned_data = super().clean()
#         employment_status = cleaned_data.get('employment_status')
#         num_children = cleaned_data.get('num_children')

#         if employment_status == 'married' and num_children is None:
#             raise forms.ValidationError("Please enter the number of children for married employees.")
#         return cleaned_data
        


    
# class salaryandbenefitsform(forms.ModelForm):
#     class Meta:
#         model = SalaryAndBenefits
#         fields = ['employee', 'base_salary', 'benefits', 'deductions', 'start_date', 'end_date']

#     widgets = {
#         'start_date': forms.DateInput(attrs={'type': 'date'}),
#         'end_date': forms.DateInput(attrs={'type': 'date'}),
#     }
