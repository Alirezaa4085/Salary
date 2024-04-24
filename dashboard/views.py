from django.shortcuts import render, get_object_or_404, redirect
from salary.models import SalaryInformation, PaymentHistory
from datetime import datetime
from django.db.models import Sum
from employee.models import Employee


def dashboard(request):
    calculate_monthly_totals(request)
    username = request.user.username
    current_user = request.user
    current_user_employees = current_user.employee_set.all()
    salary_information = SalaryInformation.objects.filter(employee__in=current_user_employees)
    payment_history = PaymentHistory.objects.filter(salary_information__in=salary_information).order_by('-payment_date')[:3]
    monthly_payments = calculate_payments_by_month(2024,request.user)
    last_three_records_employee = Employee.objects.order_by('-user')[:3]
    monthly_income_total, monthly_expenses_total = calculate_monthly_totals(request)
    total_monthly = monthly_income_total - monthly_expenses_total
    current_month = datetime.now().strftime('%B')
    current_user_employees = Employee.objects.filter(user=request.user).count()

    context = {
                'payment_history': payment_history,
                'username': username,
                'last_three_records_employee':last_three_records_employee,
                'monthly_income_total': monthly_income_total,
                'monthly_expenses_total': monthly_expenses_total,
                'current_month': current_month,
                'total_monthly':total_monthly,
                'current_user_employees':current_user_employees,
                'monthly_payments':monthly_payments
                }
    return render(request, 'dashboard.html',context)



def calculate_payments_by_month(year, user):
    monthly_payments = []
    
    for month in range(1, 13):
        # فیلتر کردن پرداخت‌ها بر اساس ماه و سال و کاربر
        payments = PaymentHistory.objects.filter(
            salary_information__salary_month__year=year,
            salary_information__salary_month__month=month,
            salary_information__employee__user=user
        )
        # محاسبه مجموع پرداخت‌های هر ماه
        total_payment = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        # اضافه کردن مجموع به لیست ماهیانه
        monthly_payments.append(total_payment)
    return monthly_payments


# current_user = request.user
# current_user_employees = current_user.employee_set.all()
# salary_information = SalaryInformation.objects.filter(employee__in=current_user_employees)
# payment_history = PaymentHistory.objects.filter(salary_information__in=salary_information).order_by('-payment_date')[:3]
    
def calculate_monthly_totals(request):
    current_user = request.user
    employees = Employee.objects.filter(user=current_user)
    current_month = datetime.now().replace(day=1)
    monthly_income_total = SalaryInformation.objects.filter(employee__in=employees, salary_month=current_month).aggregate(Sum('monthly_income'))['monthly_income__sum'] or 0
    monthly_expenses_total = SalaryInformation.objects.filter(employee__in=employees, salary_month=current_month).aggregate(Sum('monthly_expenses'))['monthly_expenses__sum'] or 0
    return monthly_income_total, monthly_expenses_total

def home(request):
    return redirect('/dashboard/')     
