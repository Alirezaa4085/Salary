from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns=[

path('employees/add/', login_required(employee_form_view), name='employee_form_view'),
path('employees/', login_required(employees_list), name='employee-list'),
path('employees/delete/<int:employee_id>/', login_required(delete_employee), name='delete_employee'),
path('employees/edit/<int:employee_id>/', edit_employee, name='edit_employee'),
    
]
