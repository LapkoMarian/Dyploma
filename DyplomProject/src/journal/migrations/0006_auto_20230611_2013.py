# Generated by Django 3.1.3 on 2023-06-11 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0005_auto_20230611_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='mark',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='journal',
            name='topik',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
