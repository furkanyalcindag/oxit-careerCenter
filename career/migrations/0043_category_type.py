# Generated by Django 3.2 on 2021-06-19 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0042_lectureapplication_scholarshipapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(max_length=128, null=True),
        ),
    ]