from django.db import models
from employee.models import Employee
from django.utils import timezone


class PaymentHistory(models.Model):
    salary_information = models.ForeignKey('SalaryInformation', on_delete=models.CASCADE)
    payment_date = models.DateField()
    payment_time = models.TimeField(default=timezone.now)
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

