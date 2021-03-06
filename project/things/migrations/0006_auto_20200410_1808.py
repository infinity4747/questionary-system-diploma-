# Generated by Django 2.2.5 on 2020-04-10 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0005_auto_20200409_1839'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='Default', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default='Default', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='test_results',
            field=models.ManyToManyField(through='things.TestResult', to='things.TestInfo'),
        ),
    ]
