# Generated by Django 2.2.5 on 2020-05-09 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('things', '0028_question_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cheatingreport',
            name='result',
            field=models.ForeignKey(default=232, on_delete=django.db.models.deletion.CASCADE, related_name='cheatings', to='things.TestResult'),
            preserve_default=False,
        ),
    ]
