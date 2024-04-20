from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companey_name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    hourly_salary = models.IntegerField(default=241286, blank=False, null=False)
    overtime_salary = models.IntegerField(default=337800, blank=False, null=False)
    the_right_of_the_child = models.IntegerField(default=5308284, blank=False, null=False)
    ben_kargari = models.IntegerField(default=10795000, blank=False, null=False)
    right_to_housing = models.IntegerField(default=8255000, blank=False, null=False)
    base_years = models.IntegerField(default=2100000, blank=False, null=False)

    def __str__(self):
        return self.user.username

class Employee(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    hire_date = models.DateField(blank = True, null = True)
    employment_status = models.BooleanField(default=False)
    num_children = models.PositiveIntegerField(default=0,blank = True)  # Set a default value
    
    def save(self, *args, **kwargs):
        # Ensure num_children is set to 0 if not provided
        if self.num_children is None:
            self.num_children = 0
        super().save(*args, **kwargs)

class SalaryInformation(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_month = models.DateField()
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    current_month_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('employee', 'salary_month')
        
    def save(self, *args, **kwargs):
        #TODO havaset be inaa bashe ke bayad dorost beshan
        # # محاسبه مجموع واریزی‌های مربوط به هر فیلد
        # total_expense_amount = Expense.objects.filter(employee=self.employee).aggregate(Sum('amount'))['amount__sum'] or 0

        # # ذخیره مجموع در فیلد monthly_expenses
        # self.monthly_expenses = total_expense_amount
        
        # محاسبه مقدار current_month_balance و ذخیره آن
        self.current_month_balance = self.monthly_income - self.monthly_expenses
        
        super().save(*args, **kwargs)
        
class Expense(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    expense_category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
        
def calculate_monthly_totals():
    # گرفتن تاریخ فعلی
    current_month = datetime.now().replace(day=1)

    # محاسبه جمع monthly_income و monthly_expenses بر اساس ماه فعلی
    monthly_income_total = SalaryInformation.objects.filter(
        salary_month=current_month
    ).aggregate(Sum('monthly_income'))['monthly_income__sum']

    monthly_expenses_total = SalaryInformation.objects.filter(
        salary_month=current_month
    ).aggregate(Sum('monthly_expenses'))['monthly_expenses__sum']

    # اگر مقادیر None باشند، آنها را به صفر تبدیل کنید
    monthly_income_total = monthly_income_total or 0
    monthly_expenses_total = monthly_expenses_total or 0

    return monthly_income_total, monthly_expenses_total


        
# class Salary(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, on_update=models.CASCADE)
#     base_salary = models.DecimalField(max_digits=10, decimal_places=2)
#     benefits = models.DecimalField(max_digits=10, decimal_places=2)
#     deductions = models.DecimalField(max_digits=10, decimal_places=2)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     def __str__(self):
#         return f"{self.employee.name} - {self.start_date} to {self.end_date}"

# class WorkHours(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     date = models.DateField()
#     daily_hours = models.DecimalField(max_digits=5, decimal_places=2)
#     weekly_hours = models.DecimalField(max_digits=5, decimal_places=2)
#     monthly_hours = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return f"{self.employee.name} - {self.date}"
