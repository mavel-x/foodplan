# Generated by Django 4.1.7 on 2023-03-18 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_auto_20230318_1309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='allergy_group',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='type',
        ),
    ]
