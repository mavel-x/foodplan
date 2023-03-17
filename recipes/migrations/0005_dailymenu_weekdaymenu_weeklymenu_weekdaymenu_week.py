# Generated by Django 4.1.7 on 2023-03-17 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_description_recipe_image_recipe_instructions'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meals', models.ManyToManyField(to='recipes.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='WeekDayMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.SmallIntegerField(choices=[(1, 'Пн'), (2, 'Вт'), (3, 'Ср'), (4, 'Чт'), (5, 'Пт'), (6, 'Сб'), (7, 'Вс')], verbose_name='день недели')),
                ('day_menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='week_day_menus', to='recipes.dailymenu', verbose_name='меню на день')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(verbose_name='пользователь')),
                ('year', models.SmallIntegerField(verbose_name='год')),
                ('week', models.SmallIntegerField(verbose_name='ISO номер недели')),
                ('daily_menus', models.ManyToManyField(through='recipes.WeekDayMenu', to='recipes.dailymenu', verbose_name='дневные меню')),
            ],
        ),
        migrations.AddField(
            model_name='weekdaymenu',
            name='week',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='week_menus', to='recipes.weeklymenu', verbose_name='недельное меню'),
        ),
    ]