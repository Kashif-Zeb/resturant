# Generated by Django 5.0.3 on 2024-03-15 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='stuid',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
