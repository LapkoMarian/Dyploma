# Generated by Django 3.1.3 on 2023-06-10 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journal',
            old_name='classroom_user_id',
            new_name='classroom_user',
        ),
    ]