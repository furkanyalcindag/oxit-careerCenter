# Generated by Django 3.2 on 2021-05-24 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0019_jobapplication'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholarship',
            name='isApprove',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='scholarship',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='career.company'),
        ),
    ]
