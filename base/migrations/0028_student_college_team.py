# Generated by Django 4.2 on 2023-05-03 08:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_student_admission'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='college',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.CreateModel(
            name='team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('team_id', models.CharField(default=uuid.uuid4, editable=False, max_length=255, unique=True)),
                ('leader', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to='base.student')),
                ('member1', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member1', to='base.student')),
                ('member2', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member2', to='base.student')),
                ('member3', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member3', to='base.student')),
                ('member4', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member4', to='base.student')),
            ],
        ),
    ]
