# Generated by Django 2.0 on 2017-12-17 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mlo_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHash',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('live_until', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='mlo_auth.User')),
            ],
        ),
    ]
