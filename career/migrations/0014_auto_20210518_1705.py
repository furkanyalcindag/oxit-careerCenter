# Generated by Django 3.2 on 2021-05-18 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0013_auto_20210517_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='isSuitable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='city',
            name='code',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
