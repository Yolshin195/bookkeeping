from django import forms
from django.db.models import Q
from django.forms import ChoiceField
from django.utils.translation import gettext_lazy as _


from transactions.models import Category, TransactionType, TransactionTypeEnum, Currency
from .models import BudgetCategory


class BudgetCategoryForm(forms.ModelForm):
    class Meta:
        model = BudgetCategory
        fields = ['category', 'currency', 'allocated_amount']
        labels = {
            'category': _('Category'),
            'currency': _('Currency'),
            'allocated_amount': _('Allocated Amount'),
        }

    def __init__(self, *args, project=None, title=_("Create Budget Category"), **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title
        self.fields['currency'].choices = self.choices_currency(project)
        self.fields['category'].choices = self.choices_category(project)
        self.fields['currency'].widget.attrs.update({'class': 'form-select col'})
        self.fields['category'].widget.attrs.update({'class': 'form-select col'})
        self.fields['allocated_amount'].widget.attrs.update({'class': 'form-control'})

    @classmethod
    def choices_category(cls, project=None):
        choices = [(None, "---------")]
        if project:
            choices.extend(cls.queryset_category(project).values_list("id", "name"))
        return choices

    @staticmethod
    def queryset_category(project=None):
        if project:
            expense_type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
            return Category.objects.filter(Q(type=expense_type) | Q(type__isnull=True), project=project)
        return Category.objects.none()

    @classmethod
    def choices_currency(cls, project=None):
        choices = [(None, "---------")]
        if project:
            choices.extend(cls.queryset_currency(project).values_list("id", "name"))
        return choices

    @staticmethod
    def queryset_currency(project=None):
        if project:
            return Currency.objects.filter(project=project)
        return Currency.objects.none()
