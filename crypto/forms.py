from django import forms
from .models import Transaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

# from django.urls import reverse_lazy


class DateInput(forms.DateInput):
    input_type = "date"


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "date",
            "exchange",
            "sold_currency_amount",
            "sold_currency",
            "sold_currency_fee",
            "bought_currency_amount",
            "bought_currency",
            "bought_currency_fee",
        )

        labels = {
            "date": "Date of transaction",
            "exchange": "Exchange",
            "sold_currency_amount": "",
            "sold_currency": "",
            "sold_currency_fee": "",
            "bought_currency_amount": "",
            "bought_currency": "",
            "bought_currency_fee": "",
        }

        widgets = {
            "date": DateInput(),
            "exchange": forms.TextInput(attrs={"placeholder": "Exchange"}),
            "sold_currency_amount": forms.TextInput(
                attrs={
                    "placeholder": "Total Amount",
                }
            ),
            "sold_currency": forms.TextInput(
                attrs={
                    "placeholder": "Fiat or Crypto",
                }
            ),
            "sold_currency_fee": forms.TextInput(
                attrs={
                    "placeholder": "Fee Amount",
                }
            ),
            "bought_currency_amount": forms.TextInput(
                attrs={
                    "placeholder": "Total Amount",
                }
            ),
            "bought_currency": forms.TextInput(
                attrs={
                    "placeholder": "Fiat or Crypto",
                }
            ),
            "bought_currency_fee": forms.TextInput(
                attrs={
                    "placeholder": "Fee Amount",
                }
            ),
        }
