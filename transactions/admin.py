from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Currency, Category, Account, TransactionType, Transaction, Project, ProjectUser


admin.site.register(Currency)
admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Account)
admin.site.register(TransactionType)
admin.site.register(Transaction)
admin.site.register(Project)
admin.site.register(ProjectUser)
