# Generated by Django 3.2 on 2021-06-23 07:07

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0043_category_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsultantCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('isDeleted', models.BooleanField(default=False)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('modificationDate', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career.category')),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career.consultant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]