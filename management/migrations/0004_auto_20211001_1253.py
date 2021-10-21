# Generated by Django 3.1.2 on 2021-10-01 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0003_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='students',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.student'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='subjects',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.subject'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subject',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
