# Generated by Django 2.0 on 2018-02-28 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rubric', '0004_auto_20180227_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubric',
            name='advice_on',
            field=models.CharField(blank=True, help_text='Юристы и адвокаты проконсультируют по…', max_length=128, verbose_name='По вопросам…'),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='title',
            field=models.CharField(blank=True, help_text='Заголовок страницы', max_length=128, verbose_name='Title'),
        ),
    ]