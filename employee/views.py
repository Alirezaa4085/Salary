from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse 
from .forms import EmployeeForm, EditEmployeeForm 
from getsalari.models import UserProfile, Employee, SalaryInformation, PaymentHistory
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Sum


#add employee
def employee_form_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

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
        form = EmployeeForm()

    return render(request, 'employee_form.html', {'form': form})

#get all employees from uniqe user
def employees_list(request):
    employees = Employee.objects.filter(user=request.user)
    return render(request, 'employees_list.html', {'employees': employees})

#delete employee
def delete_employee(request, employee_id):
    if request.method == 'DELETE':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

#edit employee details
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee-list')
    else:
        form = EditEmployeeForm(instance=employee)
    return render(request, 'employees_edit.html', {'form': form})
