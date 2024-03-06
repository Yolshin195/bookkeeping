import calendar
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from budget.services import get_categories, Filter
from transactions.models import ProjectUser


@login_required
def index(request):
    current_date = datetime.now()
    selected_month = int(request.GET.get("selected_month", default=current_date.month))
    current_year = current_date.year

    project = ProjectUser.find_project_by_user(request.user)
    categories = get_categories(Filter(
        project=project,
        month=selected_month,
        year=current_year
    ))

    context = {
        "month_name": calendar.month_name[1:],
        "selected_month": selected_month,
        "categories": categories
    }
    return render(request, "budget/index.html", context)
