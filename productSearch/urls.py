from django.contrib import admin
from django.urls import path
from . import views

app_name = "productSearch"

urlpatterns = [
    path("", views.capturecamera, name="capturecamera"),
    path("view/", views.view, name="view"),
]
