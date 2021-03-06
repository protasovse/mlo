# Generated by Django 2.0.2 on 2018-04-23 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_auto_20180423_0318'),
    ]

    operations = [
        migrations.RenameField('info', 'status', 'title'),
        migrations.AlterField(
            model_name='education',
            name='diplom',
            field=models.ImageField(blank=True, help_text='Приложите копию диплома, что бы подтвердить своё образование', upload_to='account/education/%Y/%m/', verbose_name='Копия диплома'),
        ),
    ]
