# Generated by Django 4.1.7 on 2023-03-19 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_menucategory_recipe_menu_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='menucategory',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]
