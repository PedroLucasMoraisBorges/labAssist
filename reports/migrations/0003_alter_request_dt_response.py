# Generated by Django 5.1 on 2024-09-06 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_request_dt_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='dt_response',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
