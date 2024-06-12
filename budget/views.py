from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from budget.services import get_categories, Filter, get_root_category
from transactions.forms import TransactionFilterForm
from transactions.models import ProjectUser, Account


def get_index_context(request, project):
    current_date = datetime.now()
    current_year = current_date.year

    selected_month = int(request.GET.get("month", default=current_date.month))
    selected_account = request.GET.get("account", default=Account.get_default_id(project))
    selected_owner = request.GET.get("owner", default=None)

    filter_form = TransactionFilterForm(project=project,
                                        selected_account=selected_account,
                                        selected_month=selected_month,
                                        selected_owner=selected_owner)

    budget_filter = Filter(
        project=project,
        account_id=selected_account,
        owner_id=selected_owner,
        month=selected_month,
        year=current_year
    )
    root_category = get_root_category(budget_filter)
    categories = get_categories(budget_filter)

    return {
        "budget": root_category,
        "filter_form": filter_form,
        "categories": categories
    }


@login_required
def index(request):
    project = ProjectUser.find_project_by_user(request.user)

    if project is None:
        context = {
            "budget": None,
            "filter_form": None,
            "categories": None
        }
    else:
        context = get_index_context(request, project)

    return render(request, "budget/index.html", context)
