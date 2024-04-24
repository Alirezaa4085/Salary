from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_side = models.CharField(max_length=255,default='employee', blank=False, null=False)
    hourly_salary = models.DecimalField(max_digits=10, decimal_places=0, default=241286, blank=False, null=False)
    overtime_salary = models.DecimalField(max_digits=10, decimal_places=0, default=337800, blank=False, null=False)
    the_right_of_the_child = models.DecimalField(max_digits=10, decimal_places=0, default=5308284, blank=False, null=False)
    ben_kargari = models.DecimalField(max_digits=10, decimal_places=0, default=10795000, blank=False, null=False)
    right_to_housing = models.DecimalField(max_digits=10, decimal_places=0, default=8255000, blank=False, null=False)
    base_years = models.DecimalField(max_digits=10, decimal_places=0, default=2100000, blank=False, null=False)

    def __str__(self):
        return self.user.username
