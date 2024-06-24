from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from account.models import UserProfile


# Create your models here.
class Employee(models.Model):    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_side = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    hire_date = models.DateField(blank=True, null=True)
    marital_status = models.BooleanField(default=False)
    num_children = models.PositiveIntegerField(default=0, blank=True) 
    employee_status = models.BooleanField(default=True)

    
    def save(self, *args, **kwargs):
        if self.num_children is None:
            self.num_children = 0
        super().save(*args, **kwargs)

    

@receiver(pre_save, sender=Employee)
def update_num_children(sender, instance, **kwargs):
    if instance.pk is not None:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.marital_status and not instance.marital_status:
                instance.num_children = 0
        except sender.DoesNotExist:
            pass
