# Generated by Django 5.0.3 on 2024-03-25 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resturant', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='date',
            new_name='Date',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='time',
            new_name='Time',
        ),
    ]
