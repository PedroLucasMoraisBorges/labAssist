# Generated by Django 5.1 on 2024-10-29 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0009_license_is_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='size',
            field=models.IntegerField(null=True),
        ),
    ]
