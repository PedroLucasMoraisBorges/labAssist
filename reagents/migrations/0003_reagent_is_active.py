# Generated by Django 5.1 on 2024-09-20 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reagents', '0002_alter_reagent_amount_alter_reagent_opening_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reagent',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
