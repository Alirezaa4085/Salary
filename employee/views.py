from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
from .forms import EmployeeForm, EditEmployeeForm 
from .models import Employee
from account.models import UserProfile
from django.http import JsonResponse


def employee_form_view(request):
    """
    This view renders a form for creating a new employee and
    validates the data upon POST request. If the form is valid,
    it creates a new Employee object and redirects to the list view.
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            return redirect('employee-list')
        else:
            print(form.errors)
    else:
        # Get all unique employee_side objects from UserProfile model
        # that belongs to the logged in user
        user_employee_sides = UserProfile.objects.filter(user=request.user)
        # Create a new form instance
        form = EmployeeForm()
        # set the queryset for the employee_side field to the unique employee_side objects
        form.fields['employee_side'].queryset = user_employee_sides
        # set the label for the employee_side field to the name of the employee_side object
        form.fields['employee_side'].label_from_instance = lambda obj: "%s" % obj.employee_side

    return render(request, 'employee_form.html', {'form': form})

def edit_employee(request, employee_id):
    """
    This view renders a form for editing an existing employee object
    upon POST request, it validates the data and updates the object.
    """
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, instance=employee)  # Pass instance here
        if form.is_valid():
            form.save()
            return redirect('employee-list')
    else:
        # Get all unique employee_side objects from UserProfile model
        # that belongs to the logged in user
        user_employee_sides = UserProfile.objects.filter(user=request.user)
        # Create a new form instance
        form = EditEmployeeForm(instance=employee)  # Pass instance here
        # set the queryset for the employee_side field to the unique employee_side objects
        form.fields['employee_side'].queryset = user_employee_sides
        # set the label for the employee_side field to the name of the employee_side object
        form.fields['employee_side'].label_from_instance = lambda obj: "%s" % obj.employee_side
        
    return render(request, 'employees_edit.html', {'form': form})

# get all employees from uniqe user
def employees_list(request):
    """
    This view renders the list of all employees that belong to the logged in user
    """
    employees = Employee.objects.filter(user=request.user)
    return render(request, 'employees_list.html', {'employees': employees})

def delete_employee(request, employee_id):
    """
    This view handles DELETE request to delete an employee object.
    It deletes the object and returns a success message in JSON format.
    """
    if request.method == 'DELETE':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)