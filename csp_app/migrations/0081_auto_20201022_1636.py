# Generated by Django 3.1.1 on 2020-10-22 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0080_auto_20201021_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master_candidate',
            name='ecode_status',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AlterField(
            model_name='master_candidate',
            name='loi_status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='csp_app.loi_status'),
        ),
        migrations.AlterField(
            model_name='master_candidate',
            name='vendor_status',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='csp_app.vendor_status'),
        ),
    ]