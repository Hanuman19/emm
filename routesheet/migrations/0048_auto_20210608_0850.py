# Generated by Django 3.1.5 on 2021-06-08 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0047_auto_20210602_0127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result_trail',
            old_name='doublePull',
            new_name='double',
        ),
    ]