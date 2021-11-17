from django import forms
from .models import Transaction
from datetime import date
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy


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
                    "autocomplete": "off",
                    "hx-trigger": "focus",
                    "hx-get": reverse_lazy(
                        "currencies", kwargs={"input_clicked": "sold"}
                    ),
                    "hx-target": "#results_sold",
                    "_": "on blur remove #currencies",
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
                    "autocomplete": "off",
                    "hx-trigger": "focus",
                    "hx-get": reverse_lazy(
                        "currencies", kwargs={"input_clicked": "bought"}
                    ),
                    "hx-target": "#results_bought",
                    "_": "on blur remove #currencies",
                }
            ),
            "bought_currency_fee": forms.TextInput(
                attrs={
                    "placeholder": "Fee Amount",
                }
            ),
        }

    def clean_date(self):
        data = self.cleaned_data["date"]
        if data > date.today():
            raise ValidationError("You can't enter a future transaction!")
        return data

    def clean_sold_currency_amount(self):
        data = self.cleaned_data["sold_currency_amount"]
        if data and data > 0:
            data = data * -1
        return data

    def clean_sold_currency_fee(self):
        data = self.cleaned_data["sold_currency_fee"]
        if data and data > 0:
            data = data * -1
        return data

    def clean_bought_currency_fee(self):
        data = self.cleaned_data["bought_currency_fee"]
        if data and data > 0:
            data = data * -1
        return data
