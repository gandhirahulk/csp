# Generated by Django 3.1.1 on 2020-11-22 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0011_master_candidate_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate_history',
            name='tbl_column_name',
            field=models.CharField(default='Default', max_length=100),
        ),
    ]
