from decimal import Decimal
import uuid
from dataclasses import dataclass
from django.db import models

from transactions.models import Category, ProjectLink, Project


@dataclass
class BudgetCategoryExpense:
    category__name: str
    allocated_amount: Decimal
    total_expenses: Decimal


class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.id}'


class Budget(BaseEntity, ProjectLink):
    pass


class BudgetCategory(BaseEntity, ProjectLink):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @classmethod
    def find(cls, project: Project) -> list["BudgetCategory"]:
        return cls.objects.filter(project=project)
