# Generated by Django 5.1 on 2024-10-29 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reagents', '0007_remove_reagent_amount_remove_reagent_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reagentbatch',
            name='validity',
            field=models.DateField(),
        ),
    ]
