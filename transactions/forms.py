import calendar

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Transaction, Category, Account, Currency, ProjectUser


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
        "ReferenceForm": get_reference_form(reference_model=Category),
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
    account = forms.ChoiceField(label=_("Account"), choices=[], required=False)
    month = forms.ChoiceField(label=_("Month"), choices=[], required=False)
    owner = forms.ChoiceField(label=_("Owner"), choices=[])

    def __init__(self, *args, project=None, selected_account=None, selected_month=None, selected_owner=None, **kwargs):
        super(TransactionFilterForm, self).__init__(*args, **kwargs)
        self.fields['account'].choices = self.choices_account(project)
        self.fields['month'].choices = self.choices_month()
        self.fields['owner'].choices = self.choices_owner(project)
        self.fields['account'].widget.attrs.update({'class': 'form-select', 'onchange': 'this.form.submit()'})
        self.fields['month'].widget.attrs.update({'class': 'form-select', 'onchange': 'this.form.submit()'})
        self.fields['owner'].widget.attrs.update({'class': 'form-select', 'onchange': 'this.form.submit()'})

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
    def choices_account(project=None):
        choices = [(None, _("All"))]
        if project:
            choices.extend(Account.objects.filter(project=project).values_list("id", "name"))
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

        self.fields['category'].queryset = Category.objects.filter(project=project)
        self.fields['expense_account'].queryset = Account.objects.filter(project=project)
        self.fields['expense_account'].initial = Account.get_default(project)


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

        self.fields['category'].queryset = Category.objects.filter(project=project)
        self.fields['income_account'].queryset = Account.objects.filter(project=project)


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

        self.fields['category'].queryset = Category.objects.filter(project=project)
        self.fields['expense_account'].queryset = Account.objects.filter(project=project)
        self.fields['income_account'].queryset = Account.objects.filter(project=project)
