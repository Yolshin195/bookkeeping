from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ExpenseTransactionForm, IncomeTransactionForm
from .models import Transaction, TransactionTypeEnum, TransactionType
from .reports import get_balance, get_expenses_by_day, get_expenses_by_category


def home(request):
    context = {
        "title": "test",
        "balance_report": get_balance(request.user if request.user.is_authenticated else None),
        "expenses_by_day_report": get_expenses_by_day(request.user if request.user.is_authenticated else None),
        "expenses_by_category_report": get_expenses_by_category(request.user if request.user.is_authenticated else None)
    }
    return render(request, "transactions/home.html", context)


@login_required
def index(request):
    latest_transaction_list = Transaction.objects.filter(owner=request.user).order_by("-created_at")[:5]

    context = {
        "latest_transaction_list": latest_transaction_list,
    }
    return render(request, "transactions/index.html", context)


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = ExpenseTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.owner = request.user
            form.instance.type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
            form.save()  # Сохранение новой транзакции в базе данных
            return redirect('/')  # Перенаправление после успешного создания
    else:
        form = ExpenseTransactionForm(user=request.user)

    return render(request, 'transactions/create_transaction.html', {'form': form})


@login_required
def create_income_transaction(request):
    if request.method == 'POST':
        form = IncomeTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.owner = request.user
            form.instance.type = TransactionType.find_by_code(TransactionTypeEnum.INCOME.value)
            form.save()  # Сохранение новой транзакции в базе данных
            return redirect('/')  # Перенаправление после успешного создания
    else:
        form = IncomeTransactionForm(user=request.user)

    return render(request, 'transactions/create_transaction.html', {'form': form})


@login_required
def settings(request):
    return render(request, 'transactions/settings.html')
