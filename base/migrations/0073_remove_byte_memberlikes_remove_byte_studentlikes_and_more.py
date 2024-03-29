# Generated by Django 4.2 on 2023-11-04 20:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0072_rename_likes2_byte_studentlikes_byte_memberlikes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='byte',
            name='memberLikes',
        ),
        migrations.RemoveField(
            model_name='byte',
            name='studentLikes',
        ),
        migrations.AddField(
            model_name='byte',
            name='likeOwner',
            field=models.ManyToManyField(blank=True, default='', related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
