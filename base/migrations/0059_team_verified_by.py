# Generated by Django 4.2 on 2023-09-01 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_alter_member_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='verified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verifications', to='base.member'),
        ),
    ]