# Generated by Django 3.2 on 2021-09-01 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0002_alter_urlmethod_method_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlName', models.CharField(max_length=128)),
                ('viewName', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='APIMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=128)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.api')),
            ],
        ),
        migrations.CreateModel(
            name='GroupAPIMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isAccess', models.BooleanField(default=False)),
                ('apiMethod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.apimethod')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
    ]
