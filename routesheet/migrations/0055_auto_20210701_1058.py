# Generated by Django 3.1.5 on 2021-07-01 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0054_auto_20210630_0331'),
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
