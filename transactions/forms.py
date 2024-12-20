import calendar

from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .models import Transaction, Category, Account, Currency, ProjectUser, TransactionTypeEnum, TransactionType


def get_reference_form(reference_model=None, reference_fields=None, attrs=None, choices=None, labels_fields=None):
    if reference_fields is None:
        reference_fields = []

    if attrs is None:
        attrs = {}

    if labels_fields is None:
        labels_fields = {}

    if "description" not in attrs:
        attrs["description"] = {'class': 'form-control', 'rows': 5}

    class ReferenceForm(forms.ModelForm):

        class Meta:
            model = reference_model
            fields = ["code", "name", "description", *reference_fields]
            labels = {
                "code": _("Code"),
                "name": _("Name"),
                "description": _("Description"),
                **labels_fields
            }

        def __init__(self, *args, project=None, **kwargs):
            super(ReferenceForm, self).__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update(attrs.get(field, {'class': 'form-control'}))
                if choices and field in choices:
                    model, method_name = choices[field]
                    self.fields[field].choices = getattr(self, method_name)(model, project)

        @staticmethod
        def choices_project(model, project=None):
            if project:
                return [(reference.id, reference.name) for reference in model.objects.filter(project=project)]
            return []

    return ReferenceForm


reference_form_list = {
    "Currency": {
        "Model": Currency,
        "title": _("Currency reference"),
        "ReferenceForm": get_reference_form(reference_model=Currency, reference_fields=["symbol"], labels_fields={
            "symbol": _("Symbol")
        }),
    },
    "Category": {
        "Model": Category,
        "title": _("Category reference"),
        "ReferenceForm": get_reference_form(reference_model=Category, reference_fields=["type"],
                                            labels_fields={
                                                "type": _("Type")
                                            },
                                            attrs={
                                                "type": {'class': 'form-select'},
                                            }),
    },
    "Account": {
        "Model": Account,
        "title": _("Account reference"),
        "ReferenceForm": get_reference_form(reference_model=Account, reference_fields=["currency", "is_default"],
                                            labels_fields={
                                                "currency": _("Currency"),
                                                "is_default": _("Is default")
                                            },
                                            attrs={
                                                "currency": {'class': 'form-select'},
                                                "is_default": {'class': 'form-check-input'}
                                            },
                                            choices={
                                                "currency": (Currency, "choices_project")
                                            }),
    },
}


class TransactionFilterForm(forms.Form):
    currency = forms.ChoiceField(label=_("Currency"), choices=[], required=False)
    account = forms.ChoiceField(label=_("Account"), choices=[], required=False)
    month = forms.ChoiceField(label=_("Month"), choices=[], required=False)
    owner = forms.ChoiceField(label=_("Owner"), choices=[])

    def __init__(self, *args, project=None, selected_currency=None, selected_account=None, selected_month=None, selected_owner=None, **kwargs):
        super(TransactionFilterForm, self).__init__(*args, **kwargs)
        self.fields['currency'].choices = self.choices_currency(project)
        self.fields['account'].choices = self.choices_account(project, selected_currency)
        self.fields['month'].choices = self.choices_month()
        self.fields['owner'].choices = self.choices_owner(project)
        self.fields['currency'].widget.attrs.update({'class': 'form-select', 'onchange': 'this.form.submit()'})
        self.fields['account'].widget.attrs.update({'class': 'form-select', 'onchange': 'this.form.submit()'})
        self.fields['month'].widget.attrs.update({'class': 'form-select', 'onchange': 'this.form.submit()'})
        self.fields['owner'].widget.attrs.update({'class': 'form-select', 'onchange': 'this.form.submit()'})

        if selected_currency:
            self.fields['currency'].initial = selected_currency

        if selected_month:
            self.fields['month'].initial = selected_month

        if selected_account:
            self.fields['account'].initial = selected_account

        if selected_owner:
            self.fields['owner'].initial = selected_owner

    @staticmethod
    def choices_month():
        return [(i, _(m)) for i, m, in enumerate(calendar.month_name)]

    @staticmethod
    def choices_currency(project=None):
        choices = [(None, _("All"))]
        if project:
            select = Currency.objects.filter(project=project)
            choices.extend(select.values_list("id", "name"))
        return choices

    @staticmethod
    def queryset_account(project=None, selected_currency=None):
        if project:
            queryset = Account.objects.filter(project=project)
            return queryset.filter(currency_id=selected_currency) if selected_currency else queryset
        return Category.objects.none()

    @classmethod
    def choices_account(cls, project=None, selected_currency=None):
        choices = [(None, _("All"))]
        if project:
            choices.extend(cls.queryset_account(project, selected_currency).values_list("id", "name"))
        return choices

    @staticmethod
    def choices_owner(project=None):
        choices = [(None, _("All"))]
        if project:
            choices.extend(ProjectUser.objects.filter(project=project).values_list("user__id", "user__username"))
        return choices


class ExpenseTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['expense_account', 'category', 'expense_amount', 'comment']
        labels = {
            'expense_account': _('Expense Account'),
            'category': _('Category'),
            'expense_amount': _('Expense Amount'),
            'comment': _('Comment'),
        }

    def __init__(self, *args, project=None, **kwargs):
        super(ExpenseTransactionForm, self).__init__(*args, **kwargs)
        self.title = _("Add Expense")
        self.fields['category'].widget.attrs.update({'class': 'form-select col'})
        self.fields['expense_account'].widget.attrs.update({'class': 'form-select col'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control col'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': 5})

        self.fields['category'].choices = self.choices_category(project)
        self.fields['expense_account'].choices = self.choices_account(project)
        self.fields['expense_account'].initial = Account.get_default(project)

    @staticmethod
    def choices_account(project=None):
        choices = [(None, "---------")]
        if project:
            choices.extend(Account.objects.filter(project=project).values_list("id", "name"))
        return choices

    @staticmethod
    def choices_category(project=None):
        choices = [(None, "---------")]
        if project:
            expense_type = TransactionType.find_by_code(TransactionTypeEnum.EXPENSE.value)
            choices.extend(Category.objects.filter(Q(type=expense_type) | Q(type__isnull=True), project=project).values_list("id", "name"))
        return choices


class IncomeTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['income_account', 'category', 'income_amount', 'comment']
        labels = {
            'income_account': _('Income Account'),
            'category': _('Category'),
            'income_amount': _('Income Amount'),
            'comment': _('Comment'),
        }

    def __init__(self, *args, project=None, **kwargs):
        super(IncomeTransactionForm, self).__init__(*args, **kwargs)
        self.title = _("Add Income")
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': 5})

        self.fields['category'].choices = self.choices_category(project)
        self.fields['income_account'].choices = self.choices_account(project)

    @staticmethod
    def choices_account(project=None):
        choices = [(None, "---------")]
        if project:
            choices.extend(Account.objects.filter(project=project).values_list("id", "name"))
        return choices

    @staticmethod
    def choices_category(project=None):
        choices = [(None, "---------")]
        if project:
            income_type = TransactionType.find_by_code(TransactionTypeEnum.INCOME.value)
            choices.extend(Category.objects.filter(Q(type=income_type) | Q(type__isnull=True), project=project).values_list("id", "name"))
        return choices


class TransferTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'expense_account', 'expense_amount', 'income_account', 'income_amount', 'comment']
        labels = {
            'category': _('Category'),
            'expense_account': _('Expense Account'),
            'expense_amount': _('Expense Amount'),
            'income_account': _('Income Account'),
            'income_amount': _('Income Amount'),
            'comment': _('Comment'),
        }

    def __init__(self, *args, project=None, **kwargs):
        super(TransferTransactionForm, self).__init__(*args, **kwargs)
        self.title = _("Transfer")
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['income_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': 5})

        self.fields['category'].choices = self.choices_category(project)
        self.fields['expense_account'].choices = self.choices_account(project)
        self.fields['income_account'].choices = self.choices_account(project)

    @staticmethod
    def choices_account(project=None):
        choices = [(None, "---------")]
        if project:
            choices.extend(Account.objects.filter(project=project).values_list("id", "name"))
        return choices

    @staticmethod
    def choices_category(project=None):
        choices = [(None, "---------")]
        if project:
            exchange_type = TransactionType.find_by_code(TransactionTypeEnum.EXCHANGE.value)
            choices.extend(Category.objects.filter(Q(type=exchange_type) | Q(type__isnull=True), project=project).values_list("id", "name"))
        return choices
