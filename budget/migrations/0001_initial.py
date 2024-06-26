# Generated by Django 5.0.2 on 2024-04-29 10:11

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
                ('code', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('allocated_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_default', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.project')),
            ],
            options={
                'abstract': False,
                'unique_together': {('code', 'project')},
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
