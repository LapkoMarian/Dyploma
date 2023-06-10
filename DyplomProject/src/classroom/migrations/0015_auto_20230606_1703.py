# Generated by Django 3.1.3 on 2023-06-06 14:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classroom', '0014_auto_20230605_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='users',
            field=models.ManyToManyField(related_name='classrooms', to=settings.AUTH_USER_MODEL),
        ),
    ]
