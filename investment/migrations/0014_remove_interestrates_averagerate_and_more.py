# Generated by Django 4.0.5 on 2023-01-05 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0013_alter_interestrates_averagerate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interestrates',
            name='averagerate',
        ),
        migrations.AddField(
            model_name='interestrates',
            name='averageinterestrate',
            field=models.FloatField(default=10, null=True, verbose_name='Average Interest Rate (%)'),
        ),
        migrations.CreateModel(
            name='InflationRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=8, max_length=255, null=True)),
                ('averageinflationrate', models.FloatField(default=8, null=True, verbose_name='Average Inflation Rate (%)')),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='investment.property')),
            ],
        ),
    ]