# Generated by Django 4.2.6 on 2024-01-30 06:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Finsys_App', '0010_employee_loan_transactions_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_loan_transactions',
            name='repayment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Finsys_App.employee_loan_repayment'),
        ),
    ]
