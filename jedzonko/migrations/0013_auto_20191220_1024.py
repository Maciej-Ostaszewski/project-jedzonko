# Generated by Django 3.0 on 2019-12-20 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0012_auto_20191220_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayname',
            name='day_name',
            field=models.IntegerField(choices=[(1, 'Poniedziałek'), (2, 'Wtorek'), (3, 'Środa'), (4, 'Czwartek'), (5, 'Piątek'), (6, 'Sobota'), (7, 'Niedziela')]),
        ),
    ]