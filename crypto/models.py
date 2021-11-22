from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

from datetime import date


class Transaction(models.Model):

    user = models.ForeignKey(
        get_user_model(), related_name="transactions", on_delete=models.CASCADE
    )

    exchange = models.CharField(max_length=250, blank=True)
    date = models.DateField(default=date.today)

    sold_currency = models.CharField(max_length=3)
    sold_currency_amount = models.DecimalField(
        max_digits=19, decimal_places=10, validators=[MaxValueValidator(0)]
    )

    sold_currency_fee = models.DecimalField(
        max_digits=19, decimal_places=10, blank=True, validators=[MaxValueValidator(0)]
    )
    bought_currency = models.CharField(max_length=3)
    bought_currency_amount = models.DecimalField(max_digits=19, decimal_places=10)

    bought_currency_fee = models.DecimalField(
        max_digits=19, decimal_places=10, blank=True, validators=[MaxValueValidator(0)]
    )

    price = models.DecimalField(max_digits=19, decimal_places=10)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.email} on {self.exchange} - {self.date}"

    def alt_price(self):
        price = (self.bought_currency_amount + self.bought_currency_fee) / (
            self.sold_currency_amount + self.sold_currency_fee
        )
        return price

    def save(self, *args, **kwargs):
        if not self.bought_currency_fee:
            self.bought_currency_fee = 0
        if not self.sold_currency_fee:
            self.sold_currency_fee = 0

        self.price = (self.sold_currency_amount + self.sold_currency_fee) / (
            self.bought_currency_amount + self.bought_currency_fee
        )

        super(Transaction, self).save(*args, **kwargs)
