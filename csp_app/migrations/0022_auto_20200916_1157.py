# Generated by Django 3.1.1 on 2020-09-16 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0021_auto_20200916_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_candidate',
            name='Onboarding_Spoc_Email_Id',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='master_candidate',
            name='TA_Spoc_Email_Id',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='master_candidate',
            name='location_code',
            field=models.CharField(max_length=10),
        ),
    ]
