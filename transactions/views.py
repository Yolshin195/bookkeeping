from django.shortcuts import render

from .models import Transaction


def index(request):
    latest_transaction_list = Transaction.objects.order_by("-created_at")[:5]
    context = {
        "latest_transaction_list": latest_transaction_list,
    }
    return render(request, "transactions/index.html", context)
