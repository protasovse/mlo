# Generated by Django 2.0.2 on 2018-03-30 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0022_answer_thread'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ('thread', 'pk'), 'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
    ]
