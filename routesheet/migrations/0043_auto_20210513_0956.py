# Generated by Django 3.1.5 on 2021-05-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0042_report_work_time_prostoy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result_manevr',
            name='equipment',
            field=models.IntegerField(blank=True, null=True, verbose_name='Экипировка'),
        ),
    ]