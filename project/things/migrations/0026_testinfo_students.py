# Generated by Django 2.2.5 on 2020-05-03 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0025_remove_testinfo_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='testinfo',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='tests', through='things.TestResult', to='things.Student'),
        ),
    ]
