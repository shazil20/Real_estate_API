# Generated by Django 5.0.4 on 2024-05-22 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('real_estate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='baths',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='beds',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
