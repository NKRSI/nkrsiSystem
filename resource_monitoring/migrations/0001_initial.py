# Generated by Django 3.2.16 on 2023-01-20 09:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server', models.CharField(max_length=200, verbose_name='server')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('gpu_data', models.CharField(max_length=512, verbose_name='gpu_data')),
                ('ram_data', models.CharField(max_length=512, verbose_name='ram_data')),
                ('cpu_data', models.CharField(max_length=2048, verbose_name='cpu_data')),
            ],
            options={
                'verbose_name': 'resource_usage',
                'verbose_name_plural': 'resource_usages',
            },
        ),
    ]
