# Generated by Django 5.1 on 2024-11-26 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reagents', '0011_alter_reagent_control'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reagent',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
