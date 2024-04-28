from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns=[

    path('salary/', login_required(calculate_salary), name='calculate_salary'),
    path('salary/pay/<int:SalaryInformation_id>/', login_required(salary_pay), name='salary_pay'),
    path('salary/history/<int:employee_id>/<str:month>/', login_required(monthly_payment_history), name='monthly_payment_history'),
    path('payment/delete/<int:payment_id>/', login_required(delete_payment), name='delete_payment'),

    ]
