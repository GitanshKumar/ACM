# Generated by Django 4.2 on 2023-05-05 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_remove_event_event_pics_photo_event_pics'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
