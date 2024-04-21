# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hourly_salary = models.DecimalField(max_digits=10, decimal_places=2, default=241286, blank=False, null=False)
    overtime_salary = models.DecimalField(max_digits=10, decimal_places=2, default=337800, blank=False, null=False)
    the_right_of_the_child = models.DecimalField(max_digits=10, decimal_places=2, default=5308284, blank=False, null=False)
    ben_kargari = models.DecimalField(max_digits=10, decimal_places=2, default=10795000, blank=False, null=False)
    right_to_housing = models.DecimalField(max_digits=10, decimal_places=2, default=8255000, blank=False, null=False)
    base_years = models.DecimalField(max_digits=10, decimal_places=2, default=2100000, blank=False, null=False)

    def __str__(self):
        return self.user.username


class Employee(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    hire_date = models.DateField(blank=True, null=True)
    employment_status = models.BooleanField(default=False)
    num_children = models.PositiveIntegerField(default=0, blank=True) 
    
    def save(self, *args, **kwargs):
        if self.num_children is None:
            self.num_children = 0
        super().save(*args, **kwargs)


# class SalaryInformation(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     salary_month = models.DateField()
#     monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
#     monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2)
#     current_month_balance = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         unique_together = ('employee', 'salary_month')
        
#     def save(self, *args, **kwargs):
#         self.current_month_balance = self.monthly_income - self.monthly_expenses
#         super().save(*args, **kwargs)


class PaymentHistory(models.Model):
    salary_information = models.ForeignKey('SalaryInformation', on_delete=models.CASCADE)
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class SalaryInformation(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_month = models.DateField()
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    current_month_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.current_month_balance = self.monthly_income - self.monthly_expenses
        super().save(*args, **kwargs)



class Expense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    expense_category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()


def calculate_monthly_totals():
    current_month = datetime.now().replace(day=1)
    monthly_income_total = SalaryInformation.objects.filter(salary_month=current_month).aggregate(Sum('monthly_income'))['monthly_income__sum'] or 0
    monthly_expenses_total = SalaryInformation.objects.filter(salary_month=current_month).aggregate(Sum('monthly_expenses'))['monthly_expenses__sum'] or 0
    return monthly_income_total, monthly_expenses_total
