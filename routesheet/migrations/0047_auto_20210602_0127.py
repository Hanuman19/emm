# Generated by Django 3.1.5 on 2021-06-02 01:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0046_auto_20210601_0202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result_trail',
            old_name='DoubleLokoNumber',
            new_name='doubleNumber',
        ),
        migrations.RenameField(
            model_name='result_trail',
            old_name='DoubleLokoType',
            new_name='sectionDouble',
        ),
    ]
