from django.shortcuts import render
from .models import Transaction
from .forms import TransactionForm


def home(request):

    form = TransactionForm()
    return render(request, "home.html", {"form": form})
