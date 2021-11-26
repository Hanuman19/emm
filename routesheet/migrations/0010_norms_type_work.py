# Generated by Django 3.1.5 on 2021-02-08 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0009_auto_20210208_0928'),
    ]

    operations = [
        migrations.AddField(
            model_name='norms',
            name='type_work',
            field=models.CharField(choices=[('vyvoz', 'Вывозная работа'), ('manevr', 'Маневровая работа')], default='manevr', max_length=50, verbose_name='Вид работы'),
        ),
    ]