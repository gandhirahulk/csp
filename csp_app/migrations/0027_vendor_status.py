# Generated by Django 3.1.1 on 2020-09-16 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0026_delete_vendor_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='vendor_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(auto_now_add=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
    ]