# Generated by Django 3.2 on 2021-05-31 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0028_alter_studenteducationinfo_graduationdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplication',
            name='coverLetter',
            field=models.TextField(null=True),
        ),
    ]
