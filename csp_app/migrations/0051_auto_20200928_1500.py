# Generated by Django 3.1.1 on 2020-09-28 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0050_auto_20200926_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_department',
            name='created_date_time',
            field=models.DateTimeField(blank=True),
        ),
    ]
