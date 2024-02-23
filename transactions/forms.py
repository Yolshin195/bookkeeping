from django import forms
from .models import Transaction


class ExpenseTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'expense_account', 'expense_amount']

    def __init__(self, *args, **kwargs):
        super(ExpenseTransactionForm, self).__init__(*args, **kwargs)
        self.title = "Add Expense"
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control'})


class IncomeTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'income_account', 'income_amount']

    def __init__(self, *args, **kwargs):
        super(IncomeTransactionForm, self).__init__(*args, **kwargs)
        self.title = "Add Income"
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_amount'].widget.attrs.update({'class': 'form-control'})
