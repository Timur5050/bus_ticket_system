# Generated by Django 5.0.7 on 2024-07-20 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0003_bus_facilities'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Facilities',
            new_name='Facility',
        ),
    ]
