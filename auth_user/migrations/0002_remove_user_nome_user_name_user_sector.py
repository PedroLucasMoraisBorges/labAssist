# Generated by Django 5.1 on 2024-08-28 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='nome',
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='user',
            name='sector',
            field=models.CharField(choices=[('B', 'Bolsista'), ('P', 'Professor'), ('A', 'Administração')], default='A', max_length=64),
        ),
    ]
