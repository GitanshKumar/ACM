# Generated by Django 4.2 on 2023-09-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0061_alter_news_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='year',
            field=models.CharField(choices=[('1st Year', 'First year'), ('2nd Year', 'Second year'), ('3rd Year', 'Third year'), ('4th Year', 'Fourth year'), ('Faculty', 'Faculty'), ('Alumni', 'Alumni')], default='1st', max_length=20),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.CharField(choices=[('1st Year', 'First year'), ('2nd Year', 'Second year'), ('3rd Year', 'Third year'), ('4th Year', 'Fourth year'), ('Alumni', 'Alumni')], default='1st', max_length=20),
        ),
    ]
