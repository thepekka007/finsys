# Generated by Django 4.2.6 on 2024-02-03 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Finsys_App', '0005_alter_loan_loan_duration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_loan_comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.CharField(blank=True, max_length=255, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Finsys_App.fin_company_details')),
                ('employee_loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Finsys_App.loan')),
                ('logindetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Finsys_App.fin_login_details')),
            ],
        ),
    ]
