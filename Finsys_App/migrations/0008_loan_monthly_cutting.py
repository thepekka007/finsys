# Generated by Django 4.2.6 on 2024-01-29 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finsys_App', '0007_employee_loan_repayment_employee_additional_loan'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='monthly_cutting',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
