# Generated by Django 3.2 on 2021-06-11 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_urlmethod_method_name'),
        ('career', '0040_auto_20210609_0008'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='relationField',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.urlname'),
        ),
    ]
