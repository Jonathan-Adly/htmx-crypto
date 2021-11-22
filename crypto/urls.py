from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("currencies/<str:input_clicked>", views.currencies, name="currencies"),
    path("transactions", views.transactions, name="transactions"),
    path("inline-form/<int:transaction_pk>", views.inline_form, name="inline_form"),
]
