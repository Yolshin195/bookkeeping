import uuid
from typing import Optional

from django.contrib.auth.models import User
from django.db import models

from transactions.models import Category


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
