# Generated by Django 3.0 on 2019-12-19 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0008_auto_20191219_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeplan',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals_order_in_plan', to='jedzonko.Plan'),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals_order_in_plan', to='jedzonko.Recipe'),
        ),
    ]
