from datetime import datetime, timedelta

from django.db.models import Sum, When, Case, DecimalField, F, Value
from django.db.models.functions import TruncDay

from transactions.models import Transaction, TransactionTypeEnum, TransactionType


def get_balance():
    expense_type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
    income_type = TransactionType.find_by_code(TransactionTypeEnum.INCOME.value)
    result = Transaction.objects.aggregate(
        total_expenses=Sum(Case(When(type=expense_type, then=F('expense_amount')), default=Value(0), output_field=DecimalField())),
        total_income=Sum(Case(When(type=income_type, then=F('income_amount')), default=Value(0), output_field=DecimalField())),
    )
    # Получаем значения суммы расходов и суммы доходов из результата агрегации
    total_expenses = result['total_expenses'] or 0
    total_income = result['total_income'] or 0

    # Вычисляем разницу между доходами и расходами
    difference = total_income - total_expenses
    return {
        "income": total_income,
        "expense": total_expenses,
        "difference": difference
    }


def get_expenses_by_day():
    expense_type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
    # Вычисляем начальную и конечную даты для последней недели
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Выполняем запрос на агрегацию данных
    expenses_by_day = Transaction.objects.filter(
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
