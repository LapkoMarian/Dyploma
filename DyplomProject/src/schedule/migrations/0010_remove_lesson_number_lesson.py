# Generated by Django 3.1.3 on 2023-05-07 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_lesson_number_lesson'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='number_lesson',
        ),
    ]