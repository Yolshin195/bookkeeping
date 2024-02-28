from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from budget.models import BudgetUser, Budget, BudgetCategory


@login_required
def index(request):
    budget = BudgetUser.get_current_user_budget(request.user)
    categories = BudgetCategory.find(budget)

    context = {
        "budget": budget,
        "categories": categories
    }
    return render(request, "budget/index.html", context)
