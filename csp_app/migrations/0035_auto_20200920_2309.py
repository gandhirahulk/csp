# Generated by Django 3.1.1 on 2020-09-20 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csp_app', '0034_candidate_document_document_catagory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_document',
            name='file_upload',
            field=models.FileField(upload_to='documents/'),
        ),
    ]
