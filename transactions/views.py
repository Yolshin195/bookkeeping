import calendar
import datetime

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ExpenseTransactionForm, IncomeTransactionForm, TransferTransactionForm, TransactionFilterForm
from .models import Transaction, TransactionTypeEnum, TransactionType, ProjectUser, Account
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
    current_date = datetime.datetime.now()
    project = ProjectUser.find_project_by_user(request.user)
    selected_month = int(request.GET.get("month", default=current_date.month))
    selected_account = request.GET.get("account", default=Account.get_default_id(project))

    filter_form = TransactionFilterForm(project=project,
                                        selected_account=selected_account,
                                        selected_month=selected_month)

    latest_transaction_list = Transaction.objects.filter(
        project=project,
        created_at__month=selected_month,
        created_at__year=current_date.year
    )
    if selected_account:
        latest_transaction_list = latest_transaction_list.filter(
            Q(expense_account_id=selected_account) | Q(income_account_id=selected_account)
        )
    latest_transaction_list = latest_transaction_list.order_by("-created_at")

    context = {
        "filter_form": filter_form,
        "latest_transaction_list": latest_transaction_list
    }
    return render(request, "transactions/index.html", context)


@login_required
def create_transaction(request):
    project = ProjectUser.find_project_by_user(request.user)

    if request.method == 'POST':
        form = ExpenseTransactionForm(request.POST, project=project)
        if form.is_valid():
            form.instance.owner = request.user
            form.instance.project = project
            form.instance.type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
            form.save()  # Сохранение новой транзакции в базе данных
            return redirect('/')  # Перенаправление после успешного создания
    else:
        form = ExpenseTransactionForm(project=project)

    return render(request, 'transactions/create_transaction.html', {'form': form})


@login_required
def create_income_transaction(request):
    project = ProjectUser.find_project_by_user(request.user)

    if request.method == 'POST':
        form = IncomeTransactionForm(request.POST, project=project)
        if form.is_valid():
            form.instance.owner = request.user
            form.instance.project = project
            form.instance.type = TransactionType.find_by_code(TransactionTypeEnum.INCOME.value)
            form.save()  # Сохранение новой транзакции в базе данных
            return redirect('/')  # Перенаправление после успешного создания
    else:
        form = IncomeTransactionForm(project=project)

    return render(request, 'transactions/create_transaction.html', {'form': form})


@login_required
def create_transfer_transaction(request):
    project = ProjectUser.find_project_by_user(request.user)

    if request.method == 'POST':
        form = TransferTransactionForm(request.POST, project=project)
        if form.is_valid():
            form.instance.owner = request.user
            form.instance.project = project
            form.instance.type = TransactionType.find_by_code(TransactionTypeEnum.EXCHANGE.value)
            form.save()  # Сохранение новой транзакции в базе данных
            return redirect('/')  # Перенаправление после успешного создания
    else:
        form = TransferTransactionForm(project=project)

    return render(request, 'transactions/create_transaction.html', {'form': form})


@login_required
def settings(request):
    return render(request, 'transactions/settings.html')
