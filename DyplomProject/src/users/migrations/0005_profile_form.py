# Generated by Django 3.1.3 on 2023-06-07 18:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0018_auto_20230607_1959'),
        ('users', '0004_delete_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='form',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='schedule.group'),
        ),
    ]