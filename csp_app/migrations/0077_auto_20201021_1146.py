# Generated by Django 3.1.1 on 2020-10-21 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0076_dummy_candidate_gross_salary_entered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dummy_candidate',
            name='Gross_Salary_Entered',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='offer_letter_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
        migrations.CreateModel(
            name='loi_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
        migrations.CreateModel(
            name='laptop_request_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
        migrations.CreateModel(
            name='joining_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
        migrations.CreateModel(
            name='IT_intimation_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
        migrations.CreateModel(
            name='email_creation_request_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
        migrations.CreateModel(
            name='ecode_generation_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
        migrations.CreateModel(
            name='documentation_status',
            fields=[
                ('pk_status_code', models.AutoField(primary_key=True, serialize=False)),
                ('status_name', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=100)),
                ('created_date_time', models.DateTimeField(blank=True)),
                ('modified_by', models.CharField(blank=True, max_length=100, null=True)),
                ('modified_date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='csp_app.status')),
            ],
        ),
    ]
