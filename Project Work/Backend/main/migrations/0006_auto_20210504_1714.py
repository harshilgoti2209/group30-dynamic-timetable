# Generated by Django 3.1.5 on 2021-05-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210504_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='algo',
            name='day',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='algo',
            name='time',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
