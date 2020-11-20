# Generated by Django 3.1.1 on 2020-11-20 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0009_auto_20201119_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='candidate_history',
            fields=[
                ('pk_candidate_history_code', models.AutoField(primary_key=True, serialize=False)),
                ('field_name', models.CharField(max_length=300)),
                ('old_value', models.CharField(max_length=300)),
                ('new_value', models.CharField(max_length=300)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True, null=True)),
                ('fk_candidate_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_candidate')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
    ]
