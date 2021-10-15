from blockchain.models import Order, UserAddresses


def get_available_addresses(user):
    taken_addresses = Order.objects.filter(completed=False).values_list("deposit_address", flat=True)
    return UserAddresses.objects.filter(user=user).exclude(id__in=taken_addresses)
