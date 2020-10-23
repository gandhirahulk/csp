# Generated by Django 3.1.1 on 2020-10-23 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0081_auto_20201022_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='IT_Email_ID',
            fields=[
                ('pk_email_code', models.AutoField(primary_key=True, serialize=False)),
                ('email_id', models.EmailField(default='rahul.gandhi@udaan.com', max_length=100)),
                ('created_by', models.CharField(default='sdf', max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True, null=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
    ]
