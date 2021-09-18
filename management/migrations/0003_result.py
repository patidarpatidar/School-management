# Generated by Django 3.1.2 on 2021-09-18 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20210918_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('marks', models.FloatField(default=0)),
                ('students', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.student')),
                ('subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.subject')),
            ],
        ),
    ]