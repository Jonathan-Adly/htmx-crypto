from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

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
            transactions = Transaction.objects.filter(user=request.user)[:3]
            return render(
                request,
                "components/successful_transaction.html",
                {"form": TransactionForm(), "transactions": transactions},
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


def transactions(request):
    transactions_list = Transaction.objects.filter(user=request.user)
    paginator = Paginator(transactions_list, 3)
    page_number = request.GET.get("page")
    transactions = paginator.get_page(page_number)
    return render(
        request,
        "components/transactions.html",
        {"transactions": transactions},
    )
