# Generated by Django 4.1.7 on 2023-03-18 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_weeklymenu_subscription_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weeklymenu',
            name='subscription',
        ),
    ]
