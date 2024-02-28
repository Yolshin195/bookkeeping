from django.contrib import admin
from .models import Budget, BudgetUser, BudgetCategory

admin.site.register(Budget)
admin.site.register(BudgetUser)
admin.site.register(BudgetCategory)
