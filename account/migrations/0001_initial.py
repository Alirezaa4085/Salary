# Generated by Django 5.0.4 on 2024-04-23 20:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('hourly_salary', models.DecimalField(decimal_places=0, default=241286, max_digits=10)),
                ('overtime_salary', models.DecimalField(decimal_places=0, default=337800, max_digits=10)),
                ('the_right_of_the_child', models.DecimalField(decimal_places=0, default=5308284, max_digits=10)),
                ('ben_kargari', models.DecimalField(decimal_places=0, default=10795000, max_digits=10)),
                ('right_to_housing', models.DecimalField(decimal_places=0, default=8255000, max_digits=10)),
                ('base_years', models.DecimalField(decimal_places=0, default=2100000, max_digits=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
