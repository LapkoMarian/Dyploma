# Generated by Django 3.1.3 on 2023-06-10 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0015_auto_20230606_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='users',
        ),
    ]