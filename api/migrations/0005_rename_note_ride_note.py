# Generated by Django 5.1.3 on 2024-11-21 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_ride_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ride',
            old_name='Note',
            new_name='note',
        ),
    ]
