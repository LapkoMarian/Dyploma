# Generated by Django 3.1.3 on 2023-06-10 17:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classroom', '0017_auto_20230610_2001'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='classroomusers',
            unique_together={('classroom', 'user')},
        ),
    ]