# Generated by Django 5.0.2 on 2024-03-05 16:51

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('allocated_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='budget.budget')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.category')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.project')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
