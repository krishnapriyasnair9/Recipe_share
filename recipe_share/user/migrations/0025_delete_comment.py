# Generated by Django 5.2.1 on 2025-06-09 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
