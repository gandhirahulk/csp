# Generated by Django 3.1.1 on 2020-10-31 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0088_master_vendor_group_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='group_ids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='master_vendor',
            name='group_id',
            field=models.IntegerField(),
        ),
    ]