from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    """
    A form for creating or updating an Employee instance.

    The form has a number of hidden fields that are rendered as normal input
    fields, but are not editable by the user. The fields are:

    * num_children: This field is hidden if the user is not employed, or if
      the user is employed and has entered a value for num_children. If the user
      is employed but does not have a value for num_children, then the field is
      rendered as a normal number input field.
    * hire_date: This field is rendered as a date input field with a type of
      "date".
    """

    class Meta:
        model = Employee
        fields = [
            'name',
            'employee_side',
            'phone_number',
            'address',
            'hire_date',
            'employment_status',
            'num_children',
        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['num_children'].widget = forms.HiddenInput()

        # If the user has submitted the form and the employment_status field
        # is checked, then render the num_children field as a normal number
        # input field. Otherwise, hide it.
        if 'employment_status' in self.data and self.data['employment_status'] == 'True':
            self.fields['num_children'].widget = forms.NumberInput()

        self.fields['hire_date'].widget = forms.DateInput(
            attrs={'type': 'date'}
        )
        self.fields['address'].widget = forms.Textarea(attrs={'style': 'width: 359px; height: 88px;'})



class EditEmployeeForm(forms.ModelForm):
    """
    A form for editing an existing Employee instance.

    This form has the same fields as the EmployeeForm, but it does not have
    the employee_side field because the employee_side field is not editable.
    """
    class Meta:
        model = Employee
        fields = [
            'name',
            'employee_side',
            'phone_number',
            'address',
            'hire_date',
            'employment_status',
            'num_children',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hire_date'].widget = forms.DateInput(
            attrs={'type': 'date'}
        )
        self.fields['address'].widget = forms.Textarea(attrs={'style': 'width: 359px; height: 88px;'})

