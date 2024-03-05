from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from budget.models import BudgetCategory
from transactions.models import ProjectUser


@login_required
def index(request):
    project = ProjectUser.find_project_by_user(request.user)

    context = {
        "categories": BudgetCategory.find(project)
    }
    return render(request, "budget/index.html", context)
