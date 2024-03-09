from django import forms
from .models import Transaction, Category, Account


class ExpenseTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'expense_account', 'expense_amount', 'comment']

    def __init__(self, *args, project=None, **kwargs):
        super(ExpenseTransactionForm, self).__init__(*args, **kwargs)
        self.title = "Add Expense"
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})

        self.fields['category'].queryset = Category.objects.filter(project=project)
        self.fields['expense_account'].queryset = Account.objects.filter(project=project)


class IncomeTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'income_account', 'income_amount', 'comment']

    def __init__(self, *args, project=None, **kwargs):
        super(IncomeTransactionForm, self).__init__(*args, **kwargs)
        self.title = "Add Income"
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control'})

        self.fields['category'].queryset = Category.objects.filter(project=project)
        self.fields['income_account'].queryset = Account.objects.filter(project=project)


class TransferTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'expense_account', 'expense_amount', 'income_account', 'income_amount', 'comment']

    def __init__(self, *args, project=None, **kwargs):
        super(TransferTransactionForm, self).__init__(*args, **kwargs)
        self.title = "Transfer"
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['expense_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['income_account'].widget.attrs.update({'class': 'form-select'})
        self.fields['income_amount'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 5})

        self.fields['category'].queryset = Category.objects.filter(project=project)
        self.fields['expense_account'].queryset = Account.objects.filter(project=project)
        self.fields['income_account'].queryset = Account.objects.filter(project=project)
