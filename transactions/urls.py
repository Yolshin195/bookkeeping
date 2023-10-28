from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("list", views.index, name="index"),
    path("create", views.create_transaction, name="create"),
    path("settings", views.settings, name="settings")
]
