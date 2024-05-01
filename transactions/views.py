import datetime

from django.db.models import Q, Sum, Case, When, F, Value, DecimalField
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Transaction, TransactionTypeEnum, TransactionType, ProjectUser, Account
from .reports import get_balance, get_expenses_by_day, get_expenses_by_category
from .services import Balance
from .forms import (
    ExpenseTransactionForm,
    IncomeTransactionForm,
    TransferTransactionForm,
    TransactionFilterForm,
    reference_form_list
)


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
    selected_owner = request.GET.get("owner", default=None)

    filter_form = TransactionFilterForm(project=project,
                                        selected_account=selected_account,
                                        selected_month=selected_month,
                                        selected_owner=selected_owner)

    latest_transaction = Transaction.objects.filter(
        project=project,
        created_at__month=selected_month,
        created_at__year=current_date.year
    )
    if selected_account:
        latest_transaction = latest_transaction.filter(
            Q(expense_account_id=selected_account) | Q(income_account_id=selected_account)
        )
    if selected_owner:
        latest_transaction = latest_transaction.filter(
            owner__id=selected_owner
        )
    latest_transaction_list = latest_transaction.order_by("-created_at")

    transaction_sum = latest_transaction.aggregate(
        total_expenses=Sum(Case(When(expense_account_id=selected_account, then=F('expense_amount')), default=Value(0), output_field=DecimalField())),
        total_income=Sum(Case(When(income_account_id=selected_account, then=F('income_amount')), default=Value(0), output_field=DecimalField())),
    )

    context = {
        "filter_form": filter_form,
        "latest_transaction_list": latest_transaction_list,
        "transaction_sum": transaction_sum,
        "balance": Balance.build(transaction_sum)
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


@login_required
def reference_edit(request):
    form_name = request.GET.get('form_name')
    if form_name is None:
        return redirect('reference_select')
    reference_form = reference_form_list.get(form_name)
    project = ProjectUser.find_project_by_user(request.user)

    if request.method == 'POST':
        form = reference_form["ReferenceForm"](request.POST, project=project)
        if form.is_valid():
            form.instance.owner = request.user
            form.instance.project = project
            form.save()
            return redirect('/')
    else:
        form = reference_form["ReferenceForm"](project=project)

    return render(request, 'transactions/reference/reference_edit.html', {'form': form, 'form_name': form_name})


@login_required
def reference_list(request):
    form_name = request.GET.get('form_name', None)
    if form_name is None:
        return redirect('reference_select')
    reference_form = reference_form_list.get(form_name)
    references = reference_form["Model"].objects.filter(
        project=ProjectUser.find_project_by_user(request.user)
    )
    return render(request, 'transactions/reference/reference_list.html', {
        'reference_list': references,
        "form_name": form_name
    })


@login_required
def reference_select(request):
    references = [{"name": name, "title": reference["title"]} for name, reference in reference_form_list.items()]
    return render(request, 'transactions/reference/reference_select.html', {'reference_list': references})
