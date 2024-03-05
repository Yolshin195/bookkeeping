from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN

from django.db.models import Sum, DecimalField

from budget.models import BudgetCategory
from transactions.models import Project, TransactionType, TransactionTypeEnum, Transaction


@dataclass
class BudgetCategoryExpense:
    category__name: str
    allocated_amount: Decimal
    total_expenses: Decimal
    spent: Decimal


def get_categories(project: Project) -> list[BudgetCategoryExpense]:
    budget_category_set = BudgetCategory.objects.filter(project=project).values(
        "category__code", "category__name", "allocated_amount"
    )
    expense = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
    expense_transactions = Transaction.objects.filter(type=expense, project=project)
    grouped_expense_amounts = expense_transactions.values(
        'category__code'
    ).annotate(total_amount=Sum('expense_amount', output_field=DecimalField(max_digits=10, decimal_places=2)))

    result = {}

    for budget_category in budget_category_set:
        result[budget_category.get("category__code")] = BudgetCategoryExpense(
            category__name=budget_category.get("category__name"),
            allocated_amount=budget_category.get("allocated_amount"),
            total_expenses=Decimal("0.00"),
            spent=Decimal("0.00")
        )

    for grouped_expense_amount in grouped_expense_amounts:
        if grouped_expense_amount.get("category__code") in result:
            budget_category_expense = result.get(grouped_expense_amount.get("category__code"))
            budget_category_expense.total_expenses = grouped_expense_amount.get("total_amount")
            budget_category_expense.spent = (budget_category_expense.total_expenses / budget_category_expense.allocated_amount * 100).quantize(Decimal('1'), rounding=ROUND_DOWN)

    return result.values()
