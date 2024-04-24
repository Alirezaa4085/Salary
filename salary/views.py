from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentForm 
from .models import Employee
from .models import SalaryInformation, PaymentHistory
from datetime import datetime
from django.urls import reverse
from django.db import transaction


##############---------------------------------------------------------------------------------------------------------##############

#Calculating salary for every employee
def calculate_salary(request):
    # یافتن کاربری که لاگین کرده است
    current_user = request.user

    # یافتن تمامی کارمندان مربوط به کاربر لاگین شده
    employees = Employee.objects.filter(user=current_user)

    # ایجاد یک لیست برای نگهداری اطلاعات محاسبات شده
    calculated_salaries = []

    # اجرای عملیات محاسبات برای هر کارمند
    with transaction.atomic():  # استفاده از تراکنش برای اطمینان از انجام همه عملیات با موفقیت
        current_month = datetime.now().replace(day=1)  # تاریخ اولین روز از ماه جاری
        for employee in employees:
            # محاسبه مقدارهای مورد نظر از طریق user_profile و employee
            total_salary = (
                employee.employee_side.hourly_salary * 210 +
                employee.employee_side.overtime_salary * 0 +
                employee.employee_side.the_right_of_the_child * employee.num_children +
                employee.employee_side.ben_kargari +
                employee.employee_side.right_to_housing +
                employee.employee_side.base_years
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

            # افزودن اطلاعات محاسبات شده به لیست
            calculated_salaries.append(salary_info)

    context = {
        'calculated_salaries': calculated_salaries,
    }
    return render(request, 'salary_list.html', context)

def salary_pay(request, SalaryInformation_id):
    salary_info = get_object_or_404(SalaryInformation, pk=SalaryInformation_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_date = form.cleaned_data['payment_date']  # دریافت تاریخ از فرم

            
            # Create a new PaymentHistory instance
            payment = PaymentHistory.objects.create(salary_information=salary_info, amount=amount, payment_date=payment_date)

            # Update monthly_expenses instead of total_payments
            salary_info.monthly_expenses += amount
            salary_info.save()

            return redirect('calculate_salary')  # Redirect to a success page or another page as needed
    else:
        form = PaymentForm()

    context = {'form': form}
    return render(request, 'payment_form.html', context)

def monthly_payment_history(request, employee_id, month):
    employee = get_object_or_404(Employee, id=employee_id)
    # تبدیل نام ماه به عدد ماه
    month_number = datetime.strptime(month, '%B').month
    
    # 1. استخراج همه رکوردهای مربوط به آن ماه از SalaryInformation
    salary_info_for_month = SalaryInformation.objects.filter(employee_id=employee_id, salary_month__month=month_number)
    
    # 2. استخراج پرداخت‌های مربوط به هر یک از این رکوردها
    payment_history = PaymentHistory.objects.filter(salary_information__in=salary_info_for_month)

    context = {
        'employee': employee,
        'payment_history': payment_history,
        'month': month,
    }
    return render(request, 'monthly_payment_history.html', context)

def delete_payment(request, payment_id):
    payment = get_object_or_404(PaymentHistory, pk=payment_id)
    month_expense = payment.amount  # مقدار برای کاهش ماهیانه

    # حذف پرداخت
    payment.delete()

    # به روزرسانی monthly_expenses
    salary_info = payment.salary_information
    salary_info.monthly_expenses -= month_expense
    salary_info.save()

    # ساخت URL جدید برای ماه مورد نظر
    month_url = reverse('monthly_payment_history', kwargs={'employee_id': salary_info.employee_id, 'month': salary_info.salary_month.strftime('%B').lower()})

    return redirect(month_url)

#TODO fix monthly_expenses bug

def payment_history(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    payment_history = PaymentHistory.objects.filter(salary_information__employee_id=employee_id)
    month_names = {
        'January': 'January',
        'February': 'February',
        'March': 'March',
        'April': 'April',
        'May': 'May',
        'June': 'June',
        'July': 'July',
        'August': 'August',
        'September': 'September',
        'October': 'October',
        'November': 'November',
        'December': 'December',
    }

    context = {
        'employee': employee,
        'payment_history': payment_history,
        'month_names': month_names,

    }
    return render(request, 'temp/payment_history.html', context)
