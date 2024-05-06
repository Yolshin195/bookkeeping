from django.urls import path

from . import views
from .views import create_transfer_transaction

urlpatterns = [
    path("", views.home, name="home"),
    path("transaction/list", views.index, name="index"),
    path("transaction/create/expense", views.create_transaction, name="create"),
    path("transaction/create/income", views.create_income_transaction, name="create_income_transaction"),
    path("transaction/create/transfer", create_transfer_transaction, name="create_transfer_transaction"),
    path("settings", views.settings, name="settings"),
    path('reference/edit', views.reference_edit, name="reference_edit"),
    path('reference/edit/<str:reference_id>', views.reference_edit, name="reference_edit"),
    path('reference/list', views.reference_list, name="reference_list"),
    path('reference/select', views.reference_select, name="reference_select"),
    path('reference/delete/<str:reference_id>', views.reference_delete, name="reference_delete"),
    path('project/list', views.project_list, name="project_list"),
    path('project/edit/<str:project_id>', views.project_edit, name="project_edit"),
]
