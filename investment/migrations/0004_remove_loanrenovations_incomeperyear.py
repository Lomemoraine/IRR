# Generated by Django 4.1.5 on 2023-01-31 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0003_remove_capitalgrowthrates_rate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanrenovations',
            name='incomeperyear',
        ),
    ]
