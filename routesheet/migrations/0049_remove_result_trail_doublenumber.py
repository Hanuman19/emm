# Generated by Django 3.1.5 on 2021-06-08 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0048_auto_20210608_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result_trail',
            name='doubleNumber',
        ),
    ]
