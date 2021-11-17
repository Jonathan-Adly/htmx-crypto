from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("currencies/<str:input_clicked>", views.currencies, name="currencies"),
]
