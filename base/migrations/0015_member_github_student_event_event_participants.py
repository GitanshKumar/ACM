# Generated by Django 4.2 on 2023-04-28 10:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0014_member_user_alter_member_core_alter_member_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='github',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(default='', max_length=100)),
                ('profile_pic', models.ImageField(default='images/default.png', upload_to='images/profile_pics')),
                ('linked_in', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('github', models.CharField(blank=True, default='', max_length=150, null=True)),
                ('core', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='event_participants',
            field=models.ManyToManyField(default='', related_name='participated', to='base.student'),
        ),
    ]
