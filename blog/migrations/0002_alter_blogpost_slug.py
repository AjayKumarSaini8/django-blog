# Generated by Django 5.2.3 on 2025-06-22 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True),
        ),
    ]
