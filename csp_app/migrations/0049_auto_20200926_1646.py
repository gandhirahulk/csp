# Generated by Django 3.1.1 on 2020-09-26 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0048_auto_20200926_1628'),
    ]

    operations = [
        migrations.DeleteModel(
            name='smtp_list',
        ),
        migrations.AddField(
            model_name='master_vendor',
            name='vendor_email_port',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.port_list'),
        ),
        migrations.AddField(
            model_name='master_vendor',
            name='vendor_smtp',
            field=models.CharField(default='smtp.gmail.com', max_length=100),
        ),
        migrations.AddField(
            model_name='port_list',
            name='ssl',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='port_list',
            name='tls',
            field=models.BooleanField(default=False),
        ),
    ]
