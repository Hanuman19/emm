# Generated by Django 3.1.5 on 2021-04-14 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0033_norms_thrust'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='norms',
            name='thrust',
        ),
    ]