from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse 
from .forms import EmployeeForm, EditEmployeeForm 
from .models import Employee
from account.models import UserProfile
from django.http import JsonResponse


#add employee
def employee_form_view(request):
    # user_profile, created = UserProfile.objects.get_or_create(user=request.user)

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
        # فیلتر کردن مقادیر فرم بر اساس کاربر لاگین شده
        user_employee_sides = UserProfile.objects.filter(user=request.user)
        form = EmployeeForm()
        # انتخاب تنها آیتم‌هایی که مربوط به کاربر لاگین شده است
        form.fields['employee_side'].queryset = user_employee_sides
        form.fields['employee_side'].label_from_instance = lambda obj: "%s" % obj.employee_side

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
