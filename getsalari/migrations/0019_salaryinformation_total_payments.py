# Generated by Django 5.0.4 on 2024-04-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getsalari', '0018_alter_salaryinformation_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='salaryinformation',
            name='total_payments',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]