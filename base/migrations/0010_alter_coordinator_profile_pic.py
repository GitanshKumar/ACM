# Generated by Django 4.0.4 on 2023-04-10 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_coordinator_profile_pic_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinator',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/default.png', upload_to='images/profile_pics'),
        ),
    ]
