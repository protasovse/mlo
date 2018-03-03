# Generated by Django 2.0 on 2018-03-03 06:54

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0006_auto_20180220_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(verbose_name='Текст отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.AlterField(
            model_name='likes',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='likes',
            name='entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='entry.Entry', verbose_name='Ответ'),
        ),
        migrations.AlterField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(help_text='Пользователь, который поставил отметку', on_delete=django.db.models.deletion.CASCADE, to='mlo_auth.User', verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='review',
            name='like',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='entry.Likes'),
        ),
    ]
