# Generated by Django 2.0.2 on 2018-03-21 05:14

from django.db import migrations, models
import django.db.models.fields
import timezone_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mlo_auth', '0004_user_city'),
        ('advice', '0002_auto_20180320_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezone', timezone_field.fields.TimeZoneField(default='Europe/Moscow', verbose_name='Ваша временная зона')),
                ('begin', models.TimeField(blank=True, null=True, verbose_name='Начало рабочего дня')),
                ('end', models.TimeField(blank=True, null=True, verbose_name='Конец рабочего дня')),
                ('all_time', models.BooleanField(default=True, help_text='Если не хотите принимать заявки круглосуточно, то снимите флажок и установите рабочий временной промежуток. Заявки будут приходить только в это время.', verbose_name='Принмать заявки 24 часа')),
                ('weekend', models.BooleanField(default=True, help_text='Если не хотите принимать заявки в выходные дни, то снимите флажок.', verbose_name='Принимать заявки в выходные дни')),
            ],
        ),
        migrations.AlterModelOptions(
            name='queue',
            options={'verbose_name': 'Очередь экспертов', 'verbose_name_plural': 'Очередь экспертов'},
        ),
        migrations.AlterField(
            model_name='queue',
            name='is_active',
            field=models.BooleanField(verbose_name='Активность эксперта в очереди'),
        ),
    ]
