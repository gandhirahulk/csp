# Generated by Django 3.1.1 on 2021-01-08 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('csp_app', '0016_auto_20201215_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='master_candidate',
            name='offer_letter_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]