from typing import TYPE_CHECKING
from datetime import datetime, timedelta

from django.db.models import Sum, When, Case, DecimalField, F, Value
from django.db.models.functions import TruncDay

from transactions.models import Transaction, TransactionTypeEnum, TransactionType

if TYPE_CHECKING:
    from django.contrib.auth.models import User


def get_balance(owner: "User" = None):
    labels = ['Income', 'Expense', 'Balance']
    if owner is None:
        return {
            "labels": labels,
            "data": [100000, 80000, 20000]
        }

    end_date = datetime.now()
    start_date = datetime(end_date.year, end_date.month, 1)
    expense_type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
    income_type = TransactionType.find_by_code(TransactionTypeEnum.INCOME.value)
    result = Transaction.objects.filter(
        owner=owner,
        created_at__gte=start_date,  # Учитываем только транзакции, созданные после начальной даты
        created_at__lte=end_date  # Учитываем только транзакции, созданные до конечной даты
    ).aggregate(
        total_expenses=Sum(Case(When(type=expense_type, then=F('expense_amount')), default=Value(0), output_field=DecimalField())),
        total_income=Sum(Case(When(type=income_type, then=F('income_amount')), default=Value(0), output_field=DecimalField())),
    )
    # Получаем значения суммы расходов и суммы доходов из результата агрегации
    total_expenses = result['total_expenses'] or 0
    total_income = result['total_income'] or 0

    # Вычисляем разницу между доходами и расходами
    difference = total_income - total_expenses
    return {
        "labels": labels,
        "data": [int(total_income), int(total_expenses), int(difference)]
    }


def get_expenses_by_day(owner: "User" = None):
    if owner is None:
        return {
            "labels": [1, 2, 3, 4, 5, 6],
            "data": [100000, 80000, 20000, 0, 2000, 6000]
        }

    expense_type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
    # Вычисляем начальную и конечную даты для последней недели
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Выполняем запрос на агрегацию данных
    expenses_by_day = Transaction.objects.filter(
        owner=owner,
        type=expense_type,  # Фильтруем только расходы
        created_at__gte=start_date,  # Учитываем только транзакции, созданные после начальной даты
        created_at__lte=end_date  # Учитываем только транзакции, созданные до конечной даты
    ).annotate(
        day=TruncDay('created_at')  # Группируем транзакции по дням
    ).values('day').annotate(
        total_expenses=Sum('expense_amount')  # Вычисляем сумму расходов для каждого дня
    ).order_by('day')

    return {
        "labels": [item['day'].weekday() for item in expenses_by_day],
        "data": [int(item['total_expenses']) for item in expenses_by_day]
    }


def get_expenses_by_category(owner: "User" = None):
    if owner is None:
        return {
            "labels": ["Food", "Snack", "Car"],
            "data": [100000, 80000, 50000]
        }

    expense_type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)

    end_date = datetime.now()
    start_date = datetime(end_date.year, end_date.month, 1)

    # Выполняем запрос на агрегацию данных
    expenses_by_category = Transaction.objects.filter(
        owner=owner,
        type=expense_type,  # Фильтруем только расходы
        created_at__date__gte=start_date,  # Учитываем только транзакции, созданные после начальной даты
        created_at__date__lte=end_date  # Учитываем только транзакции, созданные до конечной даты
    ).values('category__name').annotate(
        total_expenses=Sum('expense_amount')  # Вычисляем сумму расходов для каждой категории
    ).order_by('category__name')

    return {
        "labels": [item['category__name'] for item in expenses_by_category],
        "data": [int(item['total_expenses']) for item in expenses_by_category]
    }

