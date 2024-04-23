from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse 
from .forms import UserProfileForm, ExpenseForm 
from .models import UserProfile, Employee, SalaryInformation, PaymentHistory
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Sum



#Display last three payment records in template
def display_last_three_records(request):

    last_three_records = PaymentHistory.objects.select_related('salary_information__employee').order_by('-payment_date')[:3]

    context = {'last_three_records': last_three_records}
    
    return render(request, 'temp\display_payments.html', context)


# #add employee
# def employee_form_view(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     if request.method == 'POST':
#         form = EmployeeForm(request.POST)
#         if form.is_valid():
#             employee = form.save(commit=False)
#             employee.user = request.user
#             employee.save()
#             return redirect('employee-list')
#         else:
#             print(form.errors)
#     else:
#         form = EmployeeForm()

#     return render(request, 'employee_form.html', {'form': form})

def Fill_Mycompany_form(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
    form = UserProfileForm(request.POST or None, instance=user_profile)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')

    return render(request, 'profile.html', {'form': form})


def monthly_totals_json(request):
    monthly_income_total, monthly_expenses_total = calculate_monthly_totals(request)
    data = {
        'monthly_income_total': monthly_income_total,
        'monthly_expenses_total': monthly_expenses_total,
    }
    return JsonResponse(data)

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


#-------------------------------------------------------------------------------

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


# def tester(request):

#     username = request.user.username
    
#     last_three_records_salary = SalaryInformation.objects.order_by('-salary_month')[:3]
#     last_three_records_employee = Employee.objects.order_by('-user')[:3]
#     user_profile = UserProfile.objects.get(user=request.user)
#     monthly_income_total, monthly_expenses_total = calculate_monthly_totals(request)
#     total_monthly = monthly_income_total - monthly_expenses_total
#     current_month = datetime.now().strftime('%B')


#     # اطلاعات مورد نظر را به قالب ارسال کنید
#     context = {
#                 'last_three_records_salary': last_three_records_salary,
#                 'username': username,
#                 'last_three_records_employee':last_three_records_employee,
#                 'user_profile': user_profile,
#                 'monthly_income_total': monthly_income_total,
#                 'monthly_expenses_total': monthly_expenses_total,
#                 'current_month': current_month,
#                 'total_monthly':total_monthly
#                 }

#     return render(request, 'temp/dashboard2.html',context)