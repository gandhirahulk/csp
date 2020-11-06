# Generated by Django 3.1.1 on 2020-11-06 06:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='gross_salary_history',
            fields=[
                ('pk_history_code', models.AutoField(primary_key=True, serialize=False)),
                ('gross_salary_entered', models.FloatField()),
                ('gross_salary_calculated', models.FloatField()),
                ('enetered_by', models.CharField(max_length=100)),
                ('fk_candidate_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_candidate')),
                ('salary_type_selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csp_app.salary_type')),
            ],
        ),
    ]
