# Generated by Django 5.1 on 2024-10-29 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0010_request_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='movement',
            name='size',
            field=models.IntegerField(null=True),
        ),
    ]
