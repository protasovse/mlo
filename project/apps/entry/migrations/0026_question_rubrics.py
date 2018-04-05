# Generated by Django 2.0.2 on 2018-04-04 05:46

from django.db import migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rubric', '0007_auto_20180320_1005'),
        ('entry', '0025_auto_20180403_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='rubrics',
            field=mptt.fields.TreeManyToManyField(blank=True, related_name='rubrics', to='rubric.Rubric', verbose_name='Рубрики'),
        ),
    ]