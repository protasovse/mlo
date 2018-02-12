# Generated by Django 2.0 on 2018-02-12 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0006_auto_20180212_1704'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consultstatelog',
            options={'verbose_name': 'Состояние', 'verbose_name_plural': 'Состояния'},
        ),
        migrations.AlterField(
            model_name='consult',
            name='expert',
            field=models.ManyToManyField(blank=True, null=True, to='mlo_auth.User', verbose_name='Эксперт'),
        ),
        migrations.AlterField(
            model_name='consultstatelog',
            name='consult_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entry.ConsultState', verbose_name='Состояние'),
        ),
    ]
