from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="budget_main_page"),
]
