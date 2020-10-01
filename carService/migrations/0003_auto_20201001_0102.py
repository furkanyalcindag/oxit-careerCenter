# Generated by Django 3.1.1 on 2020-09-30 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carService', '0002_car_category_menu_product_productcategory_profilecar_service_serviceproduct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='birth_year',
            new_name='birthYear',
        ),
        migrations.AddField(
            model_name='profile',
            name='firmName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='isCorporate',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='taxNumber',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
