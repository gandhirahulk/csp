# Generated by Django 3.1.1 on 2020-12-14 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0012_candidate_history_tbl_column_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='master_city',
            name='fk_entity_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AddField(
            model_name='master_city',
            name='fk_region_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_region'),
        ),
        migrations.AddField(
            model_name='master_designation',
            name='fk_department_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_department'),
        ),
        migrations.AddField(
            model_name='master_designation',
            name='fk_entity_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AddField(
            model_name='master_designation',
            name='fk_function_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_function'),
        ),
        migrations.AddField(
            model_name='master_designation',
            name='fk_team_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_team'),
        ),
        migrations.AddField(
            model_name='master_function',
            name='fk_entity_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AddField(
            model_name='master_location',
            name='fk_entity_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AddField(
            model_name='master_location',
            name='fk_region_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_region'),
        ),
        migrations.AddField(
            model_name='master_location',
            name='fk_state_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_state'),
        ),
        migrations.AddField(
            model_name='master_state',
            name='fk_entity_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AddField(
            model_name='master_sub_team',
            name='fk_department_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_department'),
        ),
        migrations.AddField(
            model_name='master_sub_team',
            name='fk_entity_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AddField(
            model_name='master_sub_team',
            name='fk_function_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_function'),
        ),
        migrations.AddField(
            model_name='master_team',
            name='fk_department_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_department'),
        ),
        migrations.AddField(
            model_name='master_team',
            name='fk_entity_code',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='csp_app.master_entity'),
        ),
        migrations.AlterField(
            model_name='candidate_history',
            name='tbl_column_name',
            field=models.CharField(max_length=100),
        ),
    ]
