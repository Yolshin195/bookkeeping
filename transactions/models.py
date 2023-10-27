import uuid

from django.db import models


class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.id}'


class BaseReferenceModel(BaseEntity):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.code} - {self.name}'


class Currency(BaseReferenceModel):
    pass


class Category(BaseReferenceModel):
    pass


class Account(BaseReferenceModel):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)


class TransactionType(BaseReferenceModel):
    pass


class Transaction(BaseEntity):
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    expense_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expense_transactions',
                                        null=True, blank=True)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    income_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='income_transactions',
                                       null=True, blank=True)
    income_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'({self.type} - {self.category})'
