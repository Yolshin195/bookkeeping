from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="budget_main_page"),
    path("category/create", views.edit_budget_category, name="create_budget_category"),
    path("category/edit/<str:budget_category_id>", views.edit_budget_category, name="edit_budget_category"),
    path("category/delete/<str:budget_category_id>", views.delete_budget_category, name="delete_budget_category"),
]
