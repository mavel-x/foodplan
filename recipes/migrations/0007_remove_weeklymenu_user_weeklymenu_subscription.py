# Generated by Django 4.1.7 on 2023-03-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_dailymenu_meals_alter_weekdaymenu_day_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklymenu',
            name='user',
        ),
        migrations.AddField(
            model_name='weeklymenu',
            name='subscription',
            field=models.IntegerField(default=123123, verbose_name='подписка'),
            preserve_default=False,
        ),
    ]
