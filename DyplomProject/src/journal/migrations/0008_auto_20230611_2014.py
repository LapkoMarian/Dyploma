# Generated by Django 3.1.3 on 2023-06-11 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0007_auto_20230611_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='mark',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='journal',
            name='topik',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]