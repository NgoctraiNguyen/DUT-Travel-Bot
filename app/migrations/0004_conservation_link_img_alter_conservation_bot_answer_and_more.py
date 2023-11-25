# Generated by Django 4.2.6 on 2023-11-24 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_content_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='conservation',
            name='link_img',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='conservation',
            name='bot_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='conservation',
            name='user_question',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='content',
            name='last_tag',
            field=models.CharField(max_length=128, null=True),
        ),
    ]