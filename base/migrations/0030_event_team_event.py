# Generated by Django 4.2 on 2023-05-03 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_alter_team_member1_alter_team_member2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='team_event',
            field=models.BooleanField(default=False),
        ),
    ]
