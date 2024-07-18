from datetime import datetime
from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from budget.forms import BudgetCategoryForm
from budget.models import Budget, BudgetCategory
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


@login_required
def edit_budget_category(request, budget_category_id=None):
    project = ProjectUser.find_project_by_user(request.user)

    if budget_category_id:
        instance = get_object_or_404(BudgetCategory, id=UUID(budget_category_id))
        form = BudgetCategoryForm(
            request.POST or None, instance=instance, project=project, title=_("Edit budget category")
        )
    else:
        form = BudgetCategoryForm(request.POST or None, project=project)

    if request.method == 'POST':
        if form.is_valid():
            budget = get_object_or_404(Budget, project=project, is_default=True)
            form.instance.owner = request.user
            form.instance.project = project
            form.instance.budget = budget
            form.save()  # Сохранение новой транзакции в базе данных
            return redirect('budget_main_page')  # Перенаправление после успешного создания

    return render(request, 'budget/edit_budget_category.html', {'form': form})


@login_required
def delete_budget_category(request, budget_category_id=None):
    instance = get_object_or_404(BudgetCategory, id=UUID(budget_category_id))

    if request.method == 'POST':
        instance.delete()
        return redirect('budget_main_page')

    return render(request, 'budget/delete_budget_category.html', context={
        'title': _("Delete budget category"),
        "instance": instance
    })
