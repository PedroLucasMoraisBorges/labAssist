# Generated by Django 5.1 on 2024-09-27 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_rename_ammount_movement_amount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movement',
            options={'permissions': [('can_add_movement', 'Can add movement')]},
        ),
    ]
