# Generated by Django 5.2.1 on 2025-06-14 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_customuser_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_admin',
        ),
    ]
