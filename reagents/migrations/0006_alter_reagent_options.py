# Generated by Django 5.1 on 2024-09-24 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reagents', '0005_alter_reagent_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reagent',
            options={'permissions': [('can_add_reagent', 'Can add reagent'), ('can_change_reagent', 'Can change reagent'), ('can_delete_reagent', 'Can delete reagent'), ('can_view_reagent', 'Can view reagent')]},
        ),
    ]
