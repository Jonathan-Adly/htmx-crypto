from django.shortcuts import render
from .models import Transaction
from .forms import TransactionForm


def home(request):

    form = TransactionForm()
    return render(request, "home.html", {"form": form})


def currencies(request, input_clicked):
    return render(
        request, "components/currencies.html", {"input_clicked": input_clicked}
    )
