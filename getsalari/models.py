# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
import uuid


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hourly_salary = models.DecimalField(max_digits=10, decimal_places=0, default=241286, blank=False, null=False)
    overtime_salary = models.DecimalField(max_digits=10, decimal_places=0, default=337800, blank=False, null=False)
    the_right_of_the_child = models.DecimalField(max_digits=10, decimal_places=0, default=5308284, blank=False, null=False)
    ben_kargari = models.DecimalField(max_digits=10, decimal_places=0, default=10795000, blank=False, null=False)
    right_to_housing = models.DecimalField(max_digits=10, decimal_places=0, default=8255000, blank=False, null=False)
    base_years = models.DecimalField(max_digits=10, decimal_places=0, default=2100000, blank=False, null=False)

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


@receiver(pre_save, sender=Employee)
def update_num_children(sender, instance, **kwargs):
    if instance.pk is not None:  # چک کنید آیا این یک نمونه جدید است یا نه
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.employment_status and not instance.employment_status:
                instance.num_children = 0
        except sender.DoesNotExist:
            pass


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
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=0)

class SalaryInformation(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_month = models.DateField()
    monthly_income = models.DecimalField(max_digits=10, decimal_places=0)
    monthly_expenses = models.DecimalField(max_digits=10, decimal_places=0)
    current_month_balance = models.DecimalField(max_digits=10, decimal_places=0)

    def save(self, *args, **kwargs):
        self.current_month_balance = self.monthly_income - self.monthly_expenses
        super().save(*args, **kwargs)



class Expense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    expense_category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    expense_date = models.DateField()


