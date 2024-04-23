from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse 
from getsalari.models import UserProfile, Employee, SalaryInformation, PaymentHistory
from datetime import datetime
from django.db.models import Sum


def dashboard(request):

    username = request.user.username
    last_three_records_salary = PaymentHistory.objects.order_by('-payment_date')[:3]
    last_three_records_employee = Employee.objects.order_by('-user')[:3]
    user_profile = UserProfile.objects.get(user=request.user)
    monthly_income_total, monthly_expenses_total = calculate_monthly_totals(request)
    total_monthly = monthly_income_total - monthly_expenses_total
    current_month = datetime.now().strftime('%B')
    current_user_employees = Employee.objects.filter(user=request.user).count()

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
    return render(request, 'dashboard.html',context)

def calculate_monthly_totals(request):
    current_month = datetime.now().replace(day=1)
    # یافتن کاربر فعلی
    current_user = request.user
    # یافتن پروفایل کاربر فعلی
    user_profile = get_object_or_404(UserProfile, user=current_user)
    # فیلتر کردن اطلاعات مربوط به کاربر فعلی
    monthly_income_total = SalaryInformation.objects.filter(employee__user=current_user, salary_month=current_month).aggregate(Sum('monthly_income'))['monthly_income__sum'] or 0
    monthly_expenses_total = SalaryInformation.objects.filter(employee__user=current_user, salary_month=current_month).aggregate(Sum('monthly_expenses'))['monthly_expenses__sum'] or 0
    return monthly_income_total, monthly_expenses_total

def home(request):
    return redirect('/dashboard/')     
