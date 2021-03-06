# Generated by Django 3.1.5 on 2021-04-30 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('routesheet', '0037_auto_20210428_0311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'Меню', 'verbose_name_plural': 'Меню'},
        ),
        migrations.AddField(
            model_name='result_trail',
            name='type_loko',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='type_loko', to='routesheet.loko', verbose_name='Тип секции'),
            preserve_default=False,
        ),
    ]
