# Generated by Django 3.2 on 2021-05-17 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0012_auto_20210517_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='room',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='room',
            field=models.CharField(max_length=256, null=True),
        ),
    ]