from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ExpenseTransactionForm
from .models import Transaction


def home(request):
    context = {
        "title": "test"
    }
    return render(request, "transactions/home.html", context)


def index(request):
    latest_transaction_list = Transaction.objects.order_by("-created_at")[:5]

    context = {
        "latest_transaction_list": latest_transaction_list,
    }
    return render(request, "transactions/index.html", context)


@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = ExpenseTransactionForm(request.POST)
        if form.is_valid():
            form.save()  # Сохранение новой транзакции в базе данных
            return redirect('/')  # Перенаправление после успешного создания
    else:
        form = ExpenseTransactionForm()

    return render(request, 'transactions/create_transaction.html', {'form': form})


@login_required
def settings(request):
    return render(request, 'transactions/settings.html')
