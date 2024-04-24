from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['employee_side', 'hourly_salary', 'overtime_salary', 'the_right_of_the_child', 'ben_kargari', 'right_to_housing', 'base_years']
