# Generated by Django 4.2 on 2023-04-29 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0024_remove_event_desc_event_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='desc',
            field=models.TextField(blank=True, default="Hello, I love being in ACM's core team"),
        ),
        migrations.AlterField(
            model_name='student',
            name='desc',
            field=models.TextField(blank=True, default='Hello, I promise to be awesome!!'),
        ),
    ]
