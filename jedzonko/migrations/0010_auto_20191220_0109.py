# Generated by Django 3.0 on 2019-12-20 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0009_auto_20191220_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dayname',
            name='name',
        ),
        migrations.AddField(
            model_name='dayname',
            name='day_name',
            field=models.CharField(default=1, max_length=16),
            preserve_default=False,
        ),
    ]