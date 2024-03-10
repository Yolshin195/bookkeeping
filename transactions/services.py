from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass
class Balance:
    expense: Decimal
    expense_percent: int
    balance: Decimal
    balance_percent: int
    income: Decimal

    @classmethod
    def build(cls, data: dict) -> "Balance":
        expense = cls.get(data, "total_expenses")
        income = cls.get(data, "total_income")
        balance = income - expense
        total = income

        return Balance(
            expense=expense,
            balance=balance,
            income=income,
            expense_percent=cls.get_percent(expense, total),
            balance_percent=cls.get_percent(balance, total)
        )

    @staticmethod
    def get(data: dict, key: str) -> Decimal:
        return data.get(key, Decimal("0.00"))

    @staticmethod
    def get_percent(value: Decimal, total: Decimal) -> int:
        if value == Decimal("0.00"):
            return 0

        percent = (value / total) * Decimal("100")
        return int(percent.quantize(Decimal("1"), rounding=ROUND_HALF_UP))
