from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN
from uuid import UUID

from django.db.models import Sum, DecimalField, Q, Value

from budget.models import BudgetCategory, Budget
from transactions.models import Project, TransactionType, TransactionTypeEnum, Transaction


@dataclass
class BudgetCategoryExpense:
    id: str
    category__name: str
    allocated_amount: Decimal
    total_expenses: Decimal
    spent: Decimal


@dataclass
class Filter:
    project: Project
    currency_id: UUID | None
    account_ids: list[UUID] | None
    owner_id: UUID | None
    month: int
    year: int


def get_root_category(filter_categories: Filter) -> BudgetCategoryExpense:
    budget, _ = Budget.objects.get_or_create(project=filter_categories.project, is_default=True)

    total_expenses = {"total_amount": Decimal(0)}
    if filter_categories.account_ids:
        total_expenses = Transaction.objects.filter(
            project=filter_categories.project,
            expense_account_id__in=filter_categories.account_ids,
            created_at__month=filter_categories.month,
            created_at__year=filter_categories.year
        ).aggregate(
            total_amount=Sum('expense_amount', default=Value(0), output_field=DecimalField(max_digits=10, decimal_places=2))
        )

    # Проверка на деление на ноль
    allocated_amount = budget.allocated_amount
    if allocated_amount > 0:
        spent = (total_expenses.get("total_amount") / allocated_amount * 100).quantize(Decimal('1'), rounding=ROUND_DOWN)
    else:
        spent = Decimal('0')

    return BudgetCategoryExpense(
        id="",
        category__name="Budget",
        allocated_amount=budget.allocated_amount,
        total_expenses=total_expenses.get("total_amount"),
        spent=spent
    )


def get_categories(filter_categories: Filter) -> list[BudgetCategoryExpense]:
    budget_category_set = BudgetCategory.objects.filter(
        project=filter_categories.project
    ).values(
        "id", "category__code", "category__name", "allocated_amount"
    )
    expense = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
    expense_transactions = Transaction.objects.filter(
        type=expense,
        project=filter_categories.project,
        created_at__month=filter_categories.month,
        created_at__year=filter_categories.year
    )
    if filter_categories.account_ids:
        expense_transactions = expense_transactions.filter(
            Q(expense_account_id__in=filter_categories.account_ids) | Q(income_account_id__in=filter_categories.account_ids)
        )
    if filter_categories.owner_id:
        expense_transactions = expense_transactions.filter(
            owner__id=filter_categories.owner_id
        )
    grouped_expense_amounts = expense_transactions.values(
        'category__code'
    ).annotate(total_amount=Sum('expense_amount', output_field=DecimalField(max_digits=10, decimal_places=2)))

    result = {}

    for budget_category in budget_category_set:
        result[budget_category.get("category__code")] = BudgetCategoryExpense(
            id=str(budget_category.get("id")),
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
