from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from budget.services import get_categories
from transactions.models import ProjectUser


@login_required
def index(request):
    project = ProjectUser.find_project_by_user(request.user)

    context = {
        "categories": get_categories(project)
    }
    return render(request, "budget/index.html", context)
