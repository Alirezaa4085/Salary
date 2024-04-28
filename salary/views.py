from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentForm 
from .models import Employee
from .models import SalaryInformation, PaymentHistory
from datetime import datetime
from django.urls import reverse
from django.db import transaction


def calculate_salary(request):
    """
    Calculates the salary of the user's employees.

    Args:
        request (django.http.HttpRequest): The request sent to the server.

    Returns:
        django.http.HttpResponse: The response returned to the user.
    """
    current_user = request.user
    # Get all the employees of the current user
    employees = Employee.objects.filter(user=current_user)
    # A list to store the calculated salary information in
    calculated_salaries = []
    # Use transaction.atomic to ensure that either all or no changes are made
    # to the database
    with transaction.atomic():
        # Get the first day of the current month
        current_month = datetime.now().replace(day=1)
        # Loop through the user's employees
        for employee in employees:
            # Calculate the total salary of the employee for the current month
            total_salary = (
                employee.employee_side.hourly_salary * 210 +
                employee.employee_side.overtime_salary * 0 +
                employee.employee_side.the_right_of_the_child * employee.num_children +
                employee.employee_side.ben_kargari +
                employee.employee_side.right_to_housing +
                employee.employee_side.base_years
            )
            # Get or create a SalaryInformation instance for the employee and
            # month
            salary_info, created = SalaryInformation.objects.get_or_create(
                employee=employee,
                salary_month=current_month,
                # If the SalaryInformation instance doesn't exist, set its
                # monthly_income and monthly_expenses to the calculated values
                defaults={
                    'monthly_income': total_salary,
                    'monthly_expenses': 0,
                }
            )
            # Add the SalaryInformation instance to the list
            calculated_salaries.append(salary_info)
    # Pass the list of calculated salaries to the template
    context = {
        'calculated_salaries': calculated_salaries,
    }
    # Render the template with the context
    return render(request, 'salary_list.html', context)

def salary_pay(request, SalaryInformation_id):
    """
    View for creating a payment for a specific SalaryInformation instance.

    If the request is a POST request and the form is valid, create a new
    PaymentHistory instance with the data from the form and redirect to the
    calculate_salary view.

    If the request is a GET request or the form is not valid, render the
    payment_form.html template with the PaymentForm instance.

    Args:
        request (django.http.HttpRequest): The request sent to the server.
        SalaryInformation_id (int): The ID of the SalaryInformation instance
            to make a payment for.

    Returns:
        django.http.HttpResponse: The response returned to the user.
    """
    salary_info = get_object_or_404(SalaryInformation, pk=SalaryInformation_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_date = form.cleaned_data['payment_date']
            payment = PaymentHistory.objects.create(
                salary_information=salary_info,
                amount=amount,
                payment_date=payment_date)
            salary_info.monthly_expenses += amount
            salary_info.save()
            return redirect('calculate_salary')
    else:
        form = PaymentForm()
    context = {'form': form}
    return render(request, 'payment_form.html', context)

def monthly_payment_history(request, employee_id, month):
    """
    View for displaying the payment history for a specific employee in a
    particular month.

    Args:
        request (django.http.HttpRequest): The request sent to the server.
        employee_id (int): The ID of the employee to display payment history
            for.
        month (str): The month to display payment history for, in the format
            '%B'. For example, 'January', 'February', etc.

    Returns:
        django.http.HttpResponse: The response returned to the user.
    """
    employee = get_object_or_404(Employee, id=employee_id)
    month_number = datetime.strptime(month, '%B').month
    salary_info_for_month = SalaryInformation.objects.filter(
        employee_id=employee_id,
        salary_month__month=month_number)
    payment_history = PaymentHistory.objects.filter(
        salary_information__in=salary_info_for_month)
    context = {
        'employee': employee,
        'payment_history': payment_history,
        'month': month,
    }
    return render(request, 'monthly_payment_history.html', context)

def delete_payment(request, payment_id):
    """
    View for deleting a payment from the database

    Args:
        request (django.http.HttpRequest): The request sent to the server.
        payment_id (int): The ID of the payment to delete.

    Returns:
        django.http.HttpResponse: The response returned to the user.
    """
    payment = get_object_or_404(PaymentHistory, pk=payment_id)
    # Get the amount of the payment that is being deleted
    month_expense = payment.amount 
    # Delete the payment from the database
    payment.delete()
    # Get the salary information object that the payment is associated with
    salary_info = payment.salary_information
    # Subtract the amount of the deleted payment from the monthly expenses
    salary_info.monthly_expenses -= month_expense
    # Save the updated salary information
    salary_info.save()
    # Get the URL for the monthly payment history view
    month_url = reverse('monthly_payment_history',
                         kwargs={'employee_id': salary_info.employee_id,
                                 'month': salary_info.salary_month.strftime('%B').lower()})
    # Redirect the user to the monthly payment history view
    return redirect(month_url)
