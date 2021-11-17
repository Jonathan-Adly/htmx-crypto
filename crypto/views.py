from django.shortcuts import render
from .models import Transaction
from .forms import TransactionForm


def home(request):

    form = TransactionForm()
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return render(
                request,
                "components/successful_transaction.html",
                {"form": TransactionForm()},
            )
        else:
            return render(
                request,
                "components/transaction_form.html",
                {"form": form},
            )
    return render(request, "home.html", {"form": form})


def currencies(request, input_clicked):
    return render(
        request, "components/currencies.html", {"input_clicked": input_clicked}
    )
