# Generated by Django 4.2 on 2023-05-03 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0044_participation_remove_event_event_participants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammembership',
            name='is_leader',
            field=models.BooleanField(default=False),
        ),
    ]
