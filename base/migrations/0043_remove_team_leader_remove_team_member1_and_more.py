# Generated by Django 4.2 on 2023-05-03 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0042_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='leader',
        ),
        migrations.RemoveField(
            model_name='team',
            name='member1',
        ),
        migrations.RemoveField(
            model_name='team',
            name='member2',
        ),
        migrations.RemoveField(
            model_name='team',
            name='member3',
        ),
        migrations.RemoveField(
            model_name='team',
            name='member4',
        ),
        migrations.AddField(
            model_name='student',
            name='teams',
            field=models.ManyToManyField(blank=True, related_name='member', to='base.team'),
        ),
    ]
