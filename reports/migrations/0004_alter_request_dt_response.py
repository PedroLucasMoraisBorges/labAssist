# Generated by Django 5.1 on 2024-09-06 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_request_dt_response'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='dt_response',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
