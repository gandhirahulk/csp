# Generated by Django 3.1.1 on 2020-10-19 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0073_auto_20201019_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dummy_candidate',
            old_name='location_code',
            new_name='Gross_Salary_Entered',
        ),
        migrations.RenameField(
            model_name='master_candidate',
            old_name='location_code',
            new_name='Gross_Salary_Entered',
        ),
    ]
