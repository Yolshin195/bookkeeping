from django.urls import path

from . import views
from .views import create_transfer_transaction

urlpatterns = [
    path("", views.home, name="home"),
    path("transaction/list", views.index, name="index"),
    path("transaction/create/expense", views.create_transaction, name="create"),
    path("transaction/create/income", views.create_income_transaction, name="create_income_transaction"),
    path("transaction/create/transfer", create_transfer_transaction, name="create_transfer_transaction"),
    path("settings", views.settings, name="settings")
]
