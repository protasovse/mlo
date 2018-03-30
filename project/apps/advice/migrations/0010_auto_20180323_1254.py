# Generated by Django 2.0.2 on 2018-03-23 09:54

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('advice', '0009_scheduler_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advice',
            name='status',
            field=django_mysql.models.EnumField(choices=[('new', 'Новая'), ('paid', 'Оплачена'), ('inwork', 'В работе'), ('answered', 'Есть ответ'), ('addquestion', 'Дополнительный вопрос'), ('closed', 'Завершена'), ('canceled', 'Отменена')], db_index=True, default='new', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='statuslog',
            name='status',
            field=django_mysql.models.EnumField(choices=[('new', 'Новая'), ('paid', 'Оплачена'), ('inwork', 'В работе'), ('answered', 'Есть ответ'), ('addquestion', 'Дополнительный вопрос'), ('closed', 'Завершена'), ('canceled', 'Отменена')], db_index=True, verbose_name='Статус'),
        ),
    ]