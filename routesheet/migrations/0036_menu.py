# Generated by Django 3.1.5 on 2021-04-28 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('routesheet', '0035_result_manevr_lokonumber'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('element_type', models.CharField(choices=[('section', 'Гдавное меню'), ('element', 'подменю')], max_length=50, verbose_name='Тип элемента')),
                ('link', models.CharField(max_length=100, verbose_name='Ссылка на компонент')),
                ('region', models.ManyToManyField(to='routesheet.Region', verbose_name='Регион')),
                ('role', models.ManyToManyField(to='auth.Group', verbose_name='роли')),
                ('section', models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='LeftMenu', to='routesheet.menu', verbose_name='Меню')),
            ],
        ),
    ]