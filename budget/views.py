import calendar
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from budget.services import get_categories, Filter
from transactions.forms import TransactionFilterForm
from transactions.models import ProjectUser, Account


@login_required
def index(request):
    current_date = datetime.now()
    current_year = current_date.year

    project = ProjectUser.find_project_by_user(request.user)
    selected_month = int(request.GET.get("month", default=current_date.month))
    selected_account = request.GET.get("account", default=Account.get_default_id(project))

    filter_form = TransactionFilterForm(project=project,
                                        selected_account=selected_account,
                                        selected_month=selected_month)

    categories = get_categories(Filter(
        project=project,
        account_id=selected_account,
        month=selected_month,
        year=current_year
    ))

    context = {
        "filter_form": filter_form,
        "categories": categories
    }
    return render(request, "budget/index.html", context)
