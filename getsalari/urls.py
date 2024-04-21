from django.urls import path
from .views import *

urlpatterns = [

    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('', login_required(home), name='home'),


    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('logout/', login_required(user_logout), name='logout'),
    
    path('employees/add/', login_required(employee_form_view), name='employee_form_view'),
    path('employees/', login_required(employees_list), name='employee-list'),
    path('employees/delete/<int:employee_id>/', login_required(delete_employee), name='delete_employee'),
    path('employees/edit/<int:employee_id>/', edit_employee, name='edit_employee'),
    
    
    
    path('fillform/', login_required(Fill_companey_form), name='Fill_companey_form'),
    path('me', login_required(me) , name='me'),
    
    path('test/', login_required(display_last_three_records), name='display_salary'),

    #TODO dont trust to this urls
    
    path('tester/', login_required(tester), name='dashboard'),

    path('salary/', login_required(calculate_salary), name='calculate_salary'),
    path('salary/pay/<int:SalaryInformation_id>/', salary_pay, name='salary_pay'),
    path('salary/history/<int:employee_id>/', payment_history, name='payment_history'),


    path('add_expense/', add_expense, name='add_expense'),
    
    path('get_monthly_totals/', get_monthly_totals, name='get_monthly_totals'),


    
    # path('tester/', login_required(tester) , name='tester'),
    
    # path('employee/form/', EmployeeFormView.as_view(), name='employee_form'),
    
    # path('employees/add/', employee_create_view, name='employee_add'),
    
    
    # path('salary/', login_required(salary_list), name='salary-list'),
    
    # path('salary/add/', salary_create_view, name='salary_add'),
    
    # path('getsalary/', getsalary, name='getsalary'),

]