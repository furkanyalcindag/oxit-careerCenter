# Generated by Django 3.2 on 2021-06-08 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0038_menu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='route',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
