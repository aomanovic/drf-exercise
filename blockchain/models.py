from django.db import models
from django.conf import settings
from django.core.exceptions import NON_FIELD_ERRORS


# For search by address logging.
class SearchAddress(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=50)
    valid = models.BooleanField(default=True)


# For search by transaction logging.
class SearchTransaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    transaction = models.CharField(max_length=64)


class UserAddresses(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    address = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)


class Order(models.Model):
    SIDE_CHOICES = [
        (0, 'BUY'),
        (1, 'SELL'),
    ]

    deposit_address = models.ForeignKey(
        UserAddresses,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    amount = models.DecimalField(max_digits=40, decimal_places=18)
    pair = models.CharField(max_length=16)
    side = models.IntegerField(choices=SIDE_CHOICES)
    completed = models.BooleanField(default=False)

