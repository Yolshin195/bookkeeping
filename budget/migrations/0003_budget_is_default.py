# Generated by Django 5.0.2 on 2024-03-13 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0002_budget_allocated_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='budget',
            name='is_default',
            field=models.BooleanField(default=False),
        ),
    ]