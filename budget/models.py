import uuid
from django.db import models

from transactions.models import Category, ProjectLink


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


class ProjectReferenceModel(BaseReferenceModel, ProjectLink):

    class Meta:
        abstract = True
        unique_together = (("code", "project"),)

    @classmethod
    def find_by_code_and_project(cls, code, project):
        return cls.objects.get(code=code, project=project)


class Budget(ProjectReferenceModel):
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default and self.project:
            # Убедитесь, что только один аккаунт является дефолтным
            Budget.objects.filter(project=self.project, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class BudgetCategory(BaseEntity, ProjectLink):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
