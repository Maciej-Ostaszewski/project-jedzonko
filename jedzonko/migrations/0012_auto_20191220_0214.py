# Generated by Django 3.0 on 2019-12-20 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0011_auto_20191220_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeplan',
            name='day_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.DayName'),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Plan'),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Recipe'),
        ),
    ]
