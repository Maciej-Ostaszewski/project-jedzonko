# Generated by Django 3.0 on 2019-12-18 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0005_plan_recipes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayname',
            name='name',
            field=models.IntegerField(choices=[(1, 'Poniedziałek'), (2, 'Wtorek'), (3, 'Środa'), (4, 'Czwartek'), (5, 'Piątek'), (6, 'Sobota'), (7, 'Nedziela')]),
        ),
        migrations.AlterField(
            model_name='dayname',
            name='order',
            field=models.IntegerField(unique=True),
        ),
    ]
