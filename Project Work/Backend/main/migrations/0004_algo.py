# Generated by Django 3.1.5 on 2021-05-04 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Algo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_id', models.IntegerField()),
                ('prof_name', models.CharField(max_length=50)),
                ('prof_id', models.IntegerField()),
                ('subject', models.CharField(max_length=50)),
                ('subject_id', models.IntegerField()),
                ('batch', models.CharField(max_length=50)),
                ('batch_id', models.IntegerField()),
            ],
        ),
    ]
