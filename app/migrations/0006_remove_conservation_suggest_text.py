# Generated by Django 4.2.6 on 2023-11-25 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_conservation_suggest_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conservation',
            name='suggest_text',
        ),
    ]