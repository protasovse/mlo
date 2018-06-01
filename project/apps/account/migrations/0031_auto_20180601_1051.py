# Generated by Django 2.0.2 on 2018-06-01 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0030_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='question_rubrics',
            field=models.ManyToManyField(blank=True, help_text='Выберите рубрики из списка, уведомления о вопросах по ним будут приходить вам на электронную почту. Снимите отметки со всех рубрик, что бы не получать уведомления.', null=True, to='rubric.Rubric', verbose_name='Рубрики'),
        ),
    ]
