# Generated by Django 4.2 on 2024-02-05 14:11

import base.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0077_alter_question_belongsto_delete_eventmeta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='byte',
            name='byte',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='byte',
            name='poster',
            field=models.ImageField(blank=True, null=True, upload_to=base.models.nameBytePoster),
        ),
    ]
