# Generated by Django 5.0.6 on 2024-06-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0004_alter_projectuser_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectuser',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]