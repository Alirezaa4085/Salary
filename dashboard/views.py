from django.shortcuts import render, redirect
from salary.models import SalaryInformation, PaymentHistory
from datetime import datetime
from django.db.models import Sum
from employee.models import Employee
from django.db.models import F


# This view renders the dashboard page
# It calculates the current month's total income and expenses
# It also calculates the total amount of payments made by
# the current user in the current year
# It then passes these values to the template
def dashboard(request):
    # Calculate the total monthly income and expenses for the current user
    monthly_income_total, monthly_expenses_total = calculate_monthly_totals(request)
    
    # Calculate the total amount of payments made by the current user in the current year
    monthly_payments = calculate_payments_by_month(2024,request.user)
    
    # Get the current user's employees
    current_user = request.user
    current_user_employees = current_user.employee_set.all()
    
    # Get the latest 3 payment records and the employee who made the payment
    salary_information = SalaryInformation.objects.filter(employee__in=current_user_employees)
    payment_history = PaymentHistory.objects.filter(salary_information__in=salary_information).order_by(F('payment_date').desc(), F('payment_time').desc())[:3]
    
    # Get the latest 3 records for the current user's employees
    last_three_records_employee = Employee.objects.order_by('-user')[:3]
    
    # Get the current month in human readable form
    current_month = datetime.now().strftime('%B')
    
    # Calculate the total monthly balance
    total_monthly = monthly_income_total - monthly_expenses_total
    
    # Get the number of employees that belong to the current user
    current_user_employees = Employee.objects.filter(user=request.user).count()
    
    # Pass the values to the template
    context = {
                'payment_history': payment_history,
                'username': request.user.username,
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
    """
    Calculates the total amount of payments made by the given user
    in a specific year and month.
    
    This function first creates an empty list to store the total
    amount of payments for each month. Then it iterates through
    all the months of the given year and fetches all the payments
    made by the given user in that month and year.
    
    The function then calculates the total amount of payments
    made in that specific month and year and appends that value
    to the list. Finally, it returns the list of total payment
    amounts for each month of the given year.
    """
    monthly_payments = []
    
    for month in range(1, 13):
        payments = PaymentHistory.objects.filter(
            # Filter payments that are made in the given month and year
            salary_information__salary_month__year=year,
            salary_information__salary_month__month=month,
            # Filter payments made by the given user
            salary_information__employee__user=user
        )
        # Calculate the total amount of payments made in this month and year
        total_payment = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        # Append the total payment amount to the list
        monthly_payments.append(total_payment)
    # Return the list of total payment amounts for each month of the given year
    return monthly_payments

def calculate_monthly_totals(request):
    """
    Calculates the total monthly income and expenses for the current user.
    
    This function first gets all the employees that belong to the current user.
    It then gets the current month in a specific format that is required by
    the Django ORM to filter SalaryInformation objects.
    
    After that, it calculates the total monthly income and expenses for the
    current user by fetching all SalaryInformation objects that belong to
    the current user's employees and that are made in the current month.
    
    The function uses Django's aggregate function to calculate the sum of
    monthly income and expenses for all the SalaryInformation objects that
    match the given filter criteria.
    
    If the result of the aggregate function is None, it returns 0 instead.
    
    Finally, it returns a tuple containing the total monthly income and expenses
    for the current user.
    """
    current_user = request.user
    employees = Employee.objects.filter(user=current_user)
    current_month = datetime.now().replace(day=1)
    monthly_income_total = SalaryInformation.objects.filter(employee__in=employees, salary_month=current_month).aggregate(Sum('monthly_income'))['monthly_income__sum'] or 0
    monthly_expenses_total = SalaryInformation.objects.filter(employee__in=employees, salary_month=current_month).aggregate(Sum('monthly_expenses'))['monthly_expenses__sum'] or 0
    return monthly_income_total, monthly_expenses_total

def home(request):
    return redirect('/dashboard/')     
