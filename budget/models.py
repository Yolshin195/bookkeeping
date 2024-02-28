from decimal import Decimal
import uuid
from typing import Optional
from dataclasses import dataclass

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum

from transactions.models import Category


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


class Budget(BaseEntity):
    pass


class BudgetUser(BaseEntity):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def get_current_user_budget(cls, user: User) -> Optional[Budget]:
        try:
            budget_user = cls.objects.get(user=user)
            user_budget = budget_user.budget
            return user_budget
        except cls.DoesNotExist:
            return None


class BudgetCategory(BaseEntity):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @classmethod
    def find(cls, budget: Budget) -> list["BudgetCategory"]:
        return cls.objects.filter(budget=budget)

    @classmethod
    def budget_category_expenses(cls, budget: Budget) -> list[BudgetCategoryExpense]:
        # Получаем сумму расходов для каждой категории из BudgetCategory для всех пользователей
        return BudgetCategory.objects.filter(
            budget=budget
        ).annotate(
            total_expenses=Sum('budget__budgetuser__user__transaction__expense_amount')
        ).values('category__name', 'allocated_amount', 'total_expenses')
