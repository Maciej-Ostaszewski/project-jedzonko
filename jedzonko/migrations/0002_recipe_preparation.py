# Generated by Django 3.0 on 2019-12-18 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='preparation',
            field=models.TextField(default='jak w opisie'),
            preserve_default=False,
        ),
    ]
