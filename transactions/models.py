import uuid
from enum import Enum
from typing import Optional

from django.contrib.auth.models import User
from django.db import models


class TransactionTypeEnum(Enum):
    EXPENSE = "expense"
    INCOME = "income"
    EXCHANGE = "exchange"


class BaseEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.id}'


class BaseOwnerEntity(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class BaseReferenceModel(BaseEntity):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.code} - {self.name}'

    @classmethod
    def find_by_code(cls, code):
        return cls.objects.get(code=code)


class Project(BaseReferenceModel):
    pass


class ProjectLink(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ProjectUser(BaseEntity, ProjectLink):
    user = models.OneToOneField(User, unique=True, related_name="project_user", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project}: {self.user}'

    @classmethod
    def find_project_by_user(cls, user: User) -> Optional[Project]:
        try:
            project_user = cls.objects.get(user=user)
            return project_user.project
        except cls.DoesNotExist:
            return None


class ProjectReferenceModel(BaseReferenceModel, BaseOwnerEntity, ProjectLink):

    class Meta:
        abstract = True
        unique_together = (("code", "project"),)

    @classmethod
    def find_by_code_and_project(cls, code, project):
        return cls.objects.get(code=code, project=project)


class Currency(ProjectReferenceModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=8)


class Category(ProjectReferenceModel):
    pass


class Account(ProjectReferenceModel):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default and self.project:
            # Убедитесь, что только один аккаунт является дефолтным
            Account.objects.filter(project=self.project, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_default(cls, project: Optional[Project]) -> Optional["Account"]:
        if project is None:
            return None
        try:
            return cls.objects.get(project=project, is_default=True)
        except Account.DoesNotExist:
            return None

    @classmethod
    def get_default_id(cls, project) -> Optional[uuid.UUID]:
        account = cls.get_default(project)
        return account.id if account else None


class TransactionType(BaseReferenceModel):
    pass


class Transaction(BaseEntity, BaseOwnerEntity, ProjectLink):
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
