# Generated by Django 3.1.1 on 2020-09-26 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0045_auto_20200926_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_candidate',
            name='Date_of_Birth',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='master_candidate',
            name='Date_of_Joining',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='master_candidate',
            name='Father_Date_of_Birth',
            field=models.CharField(max_length=20),
        ),
    ]
