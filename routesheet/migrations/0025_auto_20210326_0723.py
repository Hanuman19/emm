# Generated by Django 3.1.5 on 2021-03-26 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0024_auto_20210326_0633'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='saving_saving',
            new_name='saving_trail',
        ),
    ]
