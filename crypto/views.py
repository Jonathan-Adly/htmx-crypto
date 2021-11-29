from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST, require_http_methods


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


def inline_form(request, transaction_pk):
    transaction = get_object_or_404(Transaction, pk=transaction_pk)
    inline_form = TransactionForm(instance=transaction)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            return render(
                request,
                "components/single_transaction.html",
                {"transaction": transaction},
            )
        else:
            return render(
                request,
                "components/inline_transaction_form.html",
                {
                    "inline_form": inline_form,
                    "transaction": transaction,
                    "errors": form.errors,
                },
            )

    return render(
        request,
        "components/inline_transaction_form.html",
        {"inline_form": inline_form, "transaction": transaction},
    )


@require_http_methods(["DELETE"])
def delete(request, transaction_pk):
    transaction = get_object_or_404(Transaction, pk=transaction_pk)
    transaction.delete()
    return redirect("transactions")


@require_POST
def taxable(request):
    transactions = request.POST.getlist("transaction_tax")
    query_set = []
    for item in transactions:
        transaction = Transaction.objects.get(pk=item)
        if transaction.taxable:
            transaction.taxable = False
        else:
            transaction.taxable = True
        # could do transaction.save() here, but bulk_update is faster
        query_set.append(transaction)
    Transaction.objects.bulk_update(query_set, ["taxable"])
    return redirect("transactions")
