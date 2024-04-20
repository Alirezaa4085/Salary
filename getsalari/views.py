from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm # , UserChangeForm
from django.http import JsonResponse#, HttpResponse 
from django.contrib.auth.decorators import login_required , user_passes_test
from .forms import UserProfileForm ,EmployeeForm, EditEmployeeForm,PaymentForm, ExpenseForm#, salaryandbenefitsform, testerform 
from .models import UserProfile, Employee, SalaryInformation,calculate_monthly_totals
from datetime import datetime, timedelta
from django.http import JsonResponse
import json
from django.views import View
    



# from django.views.generic.edit import FormView
# from .forms import CustomUserChangeForm, CustomPasswordChangeForm

def calculatee_salary(request):

    user_profile = get_object_or_404(UserProfile, user=request.user)
    employees = Employee.objects.filter(user=request.user)

    if not employees.exists():
        employees = []

    calculated_salaries = []
    for employee in employees:
        total_salary = (
            user_profile.hourly_salary +
            user_profile.overtime_salary +
            user_profile.the_right_of_the_child*employee.num_children +
            user_profile.ben_kargari +
            user_profile.right_to_housing +
            user_profile.base_years
        )

        calculated_salaries.append({
            'employee': employee,
            'total_salary': total_salary,
        })

    context = {
        'user_profile': user_profile,
        'calculated_salaries': calculated_salaries,
    }

    return render(request, 'salary\salary_list.html', context)

def calculate_salary(request):
    
    user_profile = get_object_or_404(UserProfile, user=request.user)
    employees = Employee.objects.filter(user=request.user)

    if not employees.exists():
        employees = []


    current_month = datetime.now().replace(day=1)  # تاریخ اولین روز از ماه جاری
    for employee in employees:
        # محاسبه مقدارهای مورد نظر از طریق user_profile و employee
        total_salary = (
            user_profile.hourly_salary * 210 +
            user_profile.overtime_salary*0 +
            user_profile.the_right_of_the_child * employee.num_children +
            user_profile.ben_kargari +
            user_profile.right_to_housing +
            user_profile.base_years
        )

        # ایجاد یک رکورد جدید در جدول SalaryInformation
        salary_info, created = SalaryInformation.objects.get_or_create(
            employee=employee,
            salary_month=current_month,
            defaults={
                'monthly_income': total_salary,  # مقدار ماهیانه درآمد محاسبه شده
                'monthly_expenses': 0,  # مقدار ماهیانه هزینه‌ها محاسبه شده (در اینجا صفر قرار داده شده است)
            }
        )

    # اطلاعات محاسبه شده را از جدول SalaryInformation بخوانید
    calculated_salaries = SalaryInformation.objects.filter(employee__user=request.user)

    context = {
        'user_profile': user_profile,
        'calculated_salaries': calculated_salaries,
    }
    return render(request, 'salary/salary_list.html', context)

def display_last_three_records(request):
    # با استفاده از Queryset، سه آخرین رکورد اضافه شده را بازیابی کنید
    last_three_records = SalaryInformation.objects.order_by('-salary_month')[:3]

    # اطلاعات مورد نظر را به قالب ارسال کنید
    context = {'last_three_records': last_three_records}
    
    # در قالب مورد نظر، از اطلاعات دریافتی برای نمایش استفاده کنید
    return render(request, 'temp\display_salary.html', context)

def me(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    print(user_profile.hourly_salary)
    return redirect('dashboard')

def user_logout(request):
    logout(request)
    return redirect('home')

def employee_form_view(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Create a new Employee instance for the user
            employee = form.save(commit=False)
            employee.user = request.user
            employee.save()
            return redirect('employee-list')
        else:
            print(form.errors)
    else:
        form = EmployeeForm()

    return render(request, 'employee_form.html', {'form': form})

def employees_list(request):
    # employees = Employee.objects.all()  # گرفتن همه کارمندان از دیتابیس
    # return render(request, 'employees/employees_list.html', {'employees': employees})
    employees = Employee.objects.filter(user=request.user)
    return render(request, 'employees/employees_list.html', {'employees': employees})

def Fill_companey_form(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    form = UserProfileForm(request.POST or None, instance=user_profile)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'profile.html', {'form': form})

def delete_employee(request, employee_id):
    if request.method == 'DELETE':
        employee = get_object_or_404(Employee, pk=employee_id)
        employee.delete()
        return JsonResponse({'message': 'Employee deleted successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)

def home(request):
    return redirect('/dashboard/')     

def login_view(request):
    form = AuthenticationForm(request, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html', {'form': form})

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html', {'form': form})

def dashboard(request):

    username = request.user.username
    
    last_three_records_salary = SalaryInformation.objects.order_by('-salary_month')[:3]
    last_three_records_employee = Employee.objects.order_by('-user')[:3]
    user_profile = UserProfile.objects.get(user=request.user)
    monthly_income_total, monthly_expenses_total = calculate_monthly_totals()
    total_monthly = monthly_income_total - monthly_expenses_total
    current_month = datetime.now().strftime('%B')
    current_user_employees = Employee.objects.filter(user=request.user).count()



    # اطلاعات مورد نظر را به قالب ارسال کنید
    context = {
                'last_three_records_salary': last_three_records_salary,
                'username': username,
                'last_three_records_employee':last_three_records_employee,
                'user_profile': user_profile,
                'monthly_income_total': monthly_income_total,
                'monthly_expenses_total': monthly_expenses_total,
                'current_month': current_month,
                'total_monthly':total_monthly,
                'current_user_employees':current_user_employees
                }

    return render(request, 'temp/dashboard2.html',context)



#TODO this views are 

def salary_pay(request, SalaryInformation_id):
    salary_info = get_object_or_404(SalaryInformation, pk=SalaryInformation_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            # Update monthly_expenses in the existing SalaryInformation instance
            salary_info.monthly_expenses = amount
            salary_info.save()

            return redirect('calculate_salary')  # Redirect to a success page or another page as needed
    else:
        form = PaymentForm()

    context = {'form': form}
    return render(request, 'temp/payment_form.html', context)

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()

            # به روز رسانی مجموع واریزی‌ها در مدل SalaryInformation مربوط به کارمند
            salary_info = SalaryInformation.objects.get(employee=form.instance.employee, salary_month=form.instance.expense_date)
            salary_info.save()

            return redirect('success_page')  # می‌توانید به یک صفحه موفقیت منتقل شوید
    else:
        form = ExpenseForm()

    return render(request, 'temp/add_expense.html', {'form': form})

def pay(request, salary_info_id):
    salary_info = get_object_or_404(SalaryInformation, id=salary_info_id)

    # انجام عملیات واریزی، به عنوان مثال اینجا یک فیلد در SalaryInformation را به True تغییر می‌دهیم
    salary_info.paid = True
    salary_info.save()

    return JsonResponse({'success': True})





# def users(request):
#     return render(request, 'users.html')


# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('home')


# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             # return redirect('change_password')
#             return redirect('dashboard')  # یا هر URL مورد نظر شما
#     else:
#         form = CustomUserChangeForm(instance=request.user)
#     return render(request, 'edit_profile.html', {'form': form})


# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = CustomPasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')  # یا هر URL مورد نظر شما
#     else:
#         form = CustomPasswordChangeForm(request.user)
#     return render(request, 'change_password.html', {'form': form})




def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EditEmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee-list')  # به نمایش لیست کارمندان منتقل می‌شود
    else:
        form = EditEmployeeForm(instance=employee)
    return render(request, 'employees/employees_edit.html', {'form': form})




# def salary_list(request):
#     salary = SalaryAndBenefits.objects.all()  # گرفتن همه کارمندان از دیتابیس
#     return render(request, 'salarysndbenefits/salarysndbenefits_list.html', {'salary': salary})


# def salary_create_view(request):
#     if request.method == 'POST':
#         form = salaryandbenefitsform(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('salary-list')  # فرض می‌کنیم که شما یک URL به این نام دارید
#     else:
#         form = salaryandbenefitsform()
#     return render(request, 'salarysndbenefits/salarysndbenefits_add.html', {'form': form})


# def add_salary_and_benefits(request):
#     if request.method == 'POST':
#         form = salaryandbenefitsform(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('salary-list')  # نام مناسبی که شما تعریف کرده‌اید
#     else:
#         form = salaryandbenefitsform()
#     return render(request, 'salarysndbenefits_add.html', {'form': form})


# def getsalary(request):
#     return render(request, 'getsalary/getsalary.html')



# def employee_form_view(request):
#     user_profile, created = Employee.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = EmployeeForm(request.POST, instance=user_profile)
#         # form = EmployeeForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employee-list')
#         else:
#             print(form.errors)
#             # انجام عملیات مورد نیاز با استفاده از اطلاعات مدل
#             # return redirect('employee-list', pk=employee.pk)
#             # return redirect('employee-list')  # فرض می‌کنیم که شما یک URL به این نام دارید
 
#     else:
#         form = EmployeeForm(instance=user_profile)

#         # form = EmployeeForm()

#     return render(request, 'employee_form.html', {'form': form})



# def employee_create_view(request):
#     if request.method == 'POST':
#         form = testerform(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('employee-list')  # فرض می‌کنیم که شما یک URL به این نام دارید
#     else:
#         form = testerform()
#     return render(request, 'employees/employees_add.html', {'form': form})



# def tester(request):
#     if request.user.is_authenticated:
#         user_profile, created = Employee.objects.get_or_create(user=request.user)
        
#         if request.method == 'POST':
#             form = testerform(request.POST, instance=user_profile)
#             if form.is_valid():
#                 form.save()
#         else:
#             form = testerform(instance=user_profile)

#         return render(request, 'user_profile.html', {'form': form})
#     else:
#         return HttpResponse("User is not authenticated.")
    
# def tester(request):
#     user_profile = Employee.objects.get_or_create(user=request.user)[0]

#     if request.method == 'POST':
#         form = testerform(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#     else:
#         form = testerform(instance=user_profile)

#     return render(request, 'user_profile.html', {'form': form})

# def tester(request):
#     user_profile, created = Employee.objects.get_or_create(user=request.user)

#     # اگر ایجاد شده است، یعنی شیء جدید ایجاد شده و باید مقداری برای hire_date تعیین شود
#     if created:
#         user_profile.hire_date = date.today()
#         user_profile.save()

#     if request.method == 'POST':
#         form = testerform(request.POST, instance=user_profile)
#         if form.is_valid():
#             form.save()
#     else:
#         form = testerform(instance=user_profile)

#     return render(request, 'user_profile.html', {'form': form})


# def tester(request):

#     @staticmethod
#     def get_data():
#         # اینجا داده‌های نمودار خود را تولید کنید
#         data = {
#             'labels': ["مورد 1", "مورد 2", "مورد 3", "مورد 4", "مورد 5"],
#             'datasets': [{
#                 'label': 'نمودار من',
#                 'backgroundColor': 'rgba(75,192,192,0.2)',
#                 'borderColor': 'rgba(75,192,192,1)',
#                 'borderWidth': 1,
#                 'data': [65 , 59, 80, 81, 56],
#             }],
#         }
#         return data

#     def get(self, request, *args, **kwargs):
#         data = self.get_data()
#         return render(request, 'temp/chart.html', {'data': json.dumps(data)})

def tester(request):

    username = request.user.username
    
    last_three_records_salary = SalaryInformation.objects.order_by('-salary_month')[:3]
    last_three_records_employee = Employee.objects.order_by('-user')[:3]
    user_profile = UserProfile.objects.get(user=request.user)
    monthly_income_total, monthly_expenses_total = calculate_monthly_totals()
    total_monthly = monthly_income_total - monthly_expenses_total
    current_month = datetime.now().strftime('%B')


    # اطلاعات مورد نظر را به قالب ارسال کنید
    context = {
                'last_three_records_salary': last_three_records_salary,
                'username': username,
                'last_three_records_employee':last_three_records_employee,
                'user_profile': user_profile,
                'monthly_income_total': monthly_income_total,
                'monthly_expenses_total': monthly_expenses_total,
                'current_month': current_month,
                'total_monthly':total_monthly
                }

    return render(request, 'temp/dashboard2.html',context)

def get_monthly_totals(request):
    # Get monthly income and expenses totals
    monthly_income_total, _ = calculate_monthly_totals()

    # Generate labels for the last 6 months (adjust as needed)
    labels = []
    current_month = datetime.now().replace(day=1)
    for i in range(6):
        labels.append(current_month.strftime('%B %Y'))
        current_month -= timedelta(days=1)
        current_month = current_month.replace(day=1)

    # Reverse the labels list to display in chronological order
    labels.reverse()

    return JsonResponse({'labels': labels, 'monthly_income_total': monthly_income_total})