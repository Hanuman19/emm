# Generated by Django 3.1.5 on 2021-03-11 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0019_auto_20210311_0424'),
    ]

    operations = [
        migrations.AddField(
            model_name='result_trail',
            name='saving',
            field=models.DecimalField(decimal_places=1, max_digits=6, null=True, verbose_name='Экономия'),
        ),
    ]
