# Generated by Django 3.2 on 2021-05-18 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0014_auto_20210518_1705'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='creationDate',
        ),
        migrations.RemoveField(
            model_name='city',
            name='isDeleted',
        ),
        migrations.RemoveField(
            model_name='city',
            name='modificationDate',
        ),
        migrations.RemoveField(
            model_name='city',
            name='uuid',
        ),
        migrations.RemoveField(
            model_name='district',
            name='creationDate',
        ),
        migrations.RemoveField(
            model_name='district',
            name='isDeleted',
        ),
        migrations.RemoveField(
            model_name='district',
            name='modificationDate',
        ),
        migrations.RemoveField(
            model_name='district',
            name='uuid',
        ),
    ]
