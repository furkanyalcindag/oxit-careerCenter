# Generated by Django 3.2 on 2021-06-04 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0032_blog_blogtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blogType',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='career.blogtype'),
        ),
    ]