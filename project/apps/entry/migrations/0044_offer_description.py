# Generated by Django 2.0.2 on 2018-06-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0043_auto_20180614_0709'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='description',
            field=models.TextField(default='', help_text='Опишите подробно суть вашей платной услуги, например: «Консультация в Skype в течении 30 мин.», «Подготовлю документы и прикреплю в ответе, или вышлю на электронный ящик.»', verbose_name='Суть предложения'),
            preserve_default=False,
        ),
    ]
