# Generated by Django 4.2 on 2023-05-05 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_team_student_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_pics',
        ),
        migrations.AddField(
            model_name='photo',
            name='event_pics',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='base.event'),
        ),
    ]
