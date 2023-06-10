# Generated by Django 3.1.3 on 2023-06-08 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0019_auto_20230608_1335'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_profile_form'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='form',
        ),
        migrations.CreateModel(
            name='StudentsForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='schedule.form')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
