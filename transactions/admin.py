from django.contrib import admin
from .models import Currency, Category, Account, TransactionType, Transaction, Project, ProjectUser


admin.site.register(Currency)
admin.site.register(Category)
admin.site.register(Account)
admin.site.register(TransactionType)
admin.site.register(Transaction)
admin.site.register(Project)
admin.site.register(ProjectUser)
