# Generated by Django 5.0.2 on 2024-03-10 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]