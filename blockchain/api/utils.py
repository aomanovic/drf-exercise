from django.db.models import Q

from blockchain.models import UserAddresses


def get_available_addresses(user, currency):
    return UserAddresses.objects.filter(Q(user=user, currency=currency) & ~Q(orders__completed=False))
