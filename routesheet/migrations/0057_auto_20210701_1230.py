# Generated by Django 3.1.5 on 2021-07-01 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0056_auto_20210701_1114'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result_manevr',
            old_name='dateEnd',
            new_name='date_end',
        ),
        migrations.RenameField(
            model_name='result_manevr',
            old_name='dateStart',
            new_name='date_start',
        ),
        migrations.RenameField(
            model_name='result_trail',
            old_name='dateEnd',
            new_name='date_end',
        ),
        migrations.RenameField(
            model_name='result_trail',
            old_name='dateStart',
            new_name='date_start',
        ),
    ]
