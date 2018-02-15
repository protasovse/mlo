# Generated by Django 2.0 on 2018-02-15 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mlo_auth', '0002_auto_20180206_0951'),
        ('entry', '0003_auto_20171218_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expert', models.ManyToManyField(blank=True, null=True, to='mlo_auth.User', verbose_name='Эксперт')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.Question')),
            ],
            options={
                'verbose_name': 'Платная консультация',
                'verbose_name_plural': 'Платные консультации',
            },
        ),
        migrations.CreateModel(
            name='ConsultState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=24, verbose_name='Название на латинице')),
                ('state', models.CharField(max_length=24, verbose_name='Название состояния')),
            ],
            options={
                'verbose_name': 'Состояние платной консультации',
                'verbose_name_plural': 'Состояния платных консультаций',
            },
        ),
        migrations.CreateModel(
            name='ConsultStateLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('consult', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.Consult')),
                ('consult_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.ConsultState', verbose_name='Состояние')),
            ],
            options={
                'verbose_name': 'Состояние',
                'verbose_name_plural': 'Состояния',
            },
        ),
        migrations.AddField(
            model_name='consult',
            name='state',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='entry.ConsultState', verbose_name='Текущее состояние'),
        ),
    ]
