"""Adressen — Widget."""

from django.urls import path

from aawidget import views

app_name = "aawidget"

urlpatterns = [
    path("opslaan/", views.opslaan, name="opslaan"),
    path("herstellen/", views.herstellen, name="herstellen"),
]
