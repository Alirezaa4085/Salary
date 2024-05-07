from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

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

    def delete(self, *args, **kwargs):
        # Prevent deletion of the default profile
        if self.user.username == 'default_user':  # Replace 'default_user' with the username of your default user
            return
        
        # Set the value of employee_side to the default value
        self.employee_side = 'employee'  # Replace 'employee' with your desired default value
        
        # Save the changes before deleting
        self.save()
        
        # Now delete the UserProfile
        super(UserProfile, self).delete(*args, **kwargs)