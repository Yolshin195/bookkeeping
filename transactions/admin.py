from django.contrib import admin
from .models import Currency, Category, Account, TransactionType, Transaction

admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(TransactionType)
admin.site.register(Transaction)
