# Generated by Django 5.1 on 2024-09-24 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reagents', '0004_alter_reagent_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reagent',
            options={'permissions': [('can_add', 'Can add reagent'), ('can_edit', 'Can edit reagent'), ('can_view', 'Can view reagents')]},
        ),
    ]
