from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required , user_passes_test


urlpatterns = [




    

    
    
    path('fillform/', login_required(Fill_Mycompany_form), name='Fill_Mycompany_form'),
    
    path('test/', login_required(display_last_three_records), name='display_salary'),


    #TODO dont trust to this urls
    
    # path('tester/', login_required(tester), name='dashboard'),
    # path('tester/', login_required(tester) , name='tester'),


    path('add_expense/', add_expense, name='add_expense'),
    
    path('get_monthly_totals/', get_monthly_totals, name='get_monthly_totals'),


    
    
    # path('employee/form/', EmployeeFormView.as_view(), name='employee_form'),
    
    # path('employees/add/', employee_create_view, name='employee_add'),
    
    
    # path('salary/', login_required(salary_list), name='salary-list'),
    
    # path('salary/add/', salary_create_view, name='salary_add'),
    
    # path('getsalary/', getsalary, name='getsalary'),

]