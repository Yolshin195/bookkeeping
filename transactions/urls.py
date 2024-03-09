from django.urls import path

from . import views
from .views import create_transfer_transaction

urlpatterns = [
    path("", views.home, name="home"),
    path("list", views.index, name="index"),
    path("create", views.create_transaction, name="create"),
    path("create/income", views.create_income_transaction, name="create_income_transaction"),
    path("create/transfer", create_transfer_transaction, name="create_transfer_transaction"),
    path("settings", views.settings, name="settings")
]
