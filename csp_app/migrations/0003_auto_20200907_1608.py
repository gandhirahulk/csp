# Generated by Django 3.1.1 on 2020-09-07 10:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0002_auto_20200907_1206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='master_department',
            name='fk_agency_code',
        ),
        migrations.AddField(
            model_name='master_department',
            name='fk_entity_code',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AlterField(
            model_name='master_agency',
            name='agency_email_id',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='master_agency',
            name='agency_email_id_password',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='master_agency',
            name='agency_phone_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='master_agency',
            name='spoc_name',
            field=models.CharField(max_length=50),
        ),
    ]
