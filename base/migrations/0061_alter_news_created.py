# Generated by Django 4.2 on 2023-09-01 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0060_alter_news_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='created',
            field=models.DateTimeField(),
        ),
    ]
