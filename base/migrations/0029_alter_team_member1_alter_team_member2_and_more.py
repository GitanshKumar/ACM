# Generated by Django 4.2 on 2023-05-03 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_student_college_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='member1',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member1', to='base.student'),
        ),
        migrations.AlterField(
            model_name='team',
            name='member2',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member2', to='base.student'),
        ),
        migrations.AlterField(
            model_name='team',
            name='member3',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member3', to='base.student'),
        ),
        migrations.AlterField(
            model_name='team',
            name='member4',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member4', to='base.student'),
        ),
    ]
