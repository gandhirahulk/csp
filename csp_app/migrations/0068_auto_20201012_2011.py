# Generated by Django 3.1.1 on 2020-10-12 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0067_auto_20201007_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary_structure',
            name='annual_fixed_salary',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='salary_structure',
            name='fixed_salary',
            field=models.FloatField(default=0),
        ),
    ]
