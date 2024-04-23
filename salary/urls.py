from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


urlpatterns=[

    path('salary/', login_required(calculate_salary), name='calculate_salary'),
    path('salary/pay/<int:SalaryInformation_id>/', salary_pay, name='salary_pay'),
    path('salary/history/<int:employee_id>/', payment_history, name='payment_history'),
    path('salary/history/<int:employee_id>/<str:month>/', monthly_payment_history, name='monthly_payment_history'),
    path('payment/delete/<int:payment_id>/', delete_payment, name='delete_payment'),

]
