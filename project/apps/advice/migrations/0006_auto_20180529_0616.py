# Generated by Django 2.0.2 on 2018-05-29 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advice', '0005_auto_20180529_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advice',
            name='overdue_date',
            field=models.DateTimeField(blank=True, help_text='Время, когда заявка будет считаться просроченной и назначен новый эксперт', null=True),
        ),
    ]