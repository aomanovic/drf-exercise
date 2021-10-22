from django.db.models import Q
from rest_framework import serializers

from blockchain.api.utils import get_available_addresses
from blockchain.models import Order, SearchAddress, SearchTransaction, UserAddresses
from rest_framework.validators import UniqueTogetherValidator


class SearchAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchAddress
        fields = ['timestamp', 'user', 'address', 'valid']


class SearchTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTransaction
        fields = ['user', 'transaction']


class UserAddressesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddresses
        fields = ['user', 'address', 'currency']
        validators = [
            UniqueTogetherValidator(
                queryset=UserAddresses.objects.all(),
                fields=['user', 'address'],
                message="Address is already marked as mine."
            )
        ]

    def validate(self, value):
        addresses = [i.address for i in SearchAddress.objects.filter(user=value['user']).all()]
        if value['address'] not in addresses:
            raise serializers.ValidationError("Address has not been searched")
        addresses = [i.address for i in SearchAddress.objects.filter(user=value['user'], valid=True).all()]
        if value['address'] not in addresses:
            raise serializers.ValidationError("Invalid active address")
        return value


class OrderSerializer(serializers.ModelSerializer):
    deposit_address = UserAddressesSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'amount', 'deposit_address', 'pair', 'side', 'completed']
        read_only_fields = ['id', 'deposit_address', 'completed']

    def __init__(self, *args, **kwargs):
        super(OrderSerializer, self).__init__(*args, **kwargs)
        data = kwargs.get("data", None)
        if data and "pair" in data and 'side' in data:
            currencies_in_pair = data['pair'].split("/")
            base_currency = currencies_in_pair[0]
            quote_currency = currencies_in_pair[1]
            deposit_address_currency = base_currency if data['side'] == 1 else quote_currency
            self.available_addresses = get_available_addresses(self.context["user"], deposit_address_currency)

    def validate(self, value):
        if not self.available_addresses.exists():
            raise serializers.ValidationError("There are no available addresses")

        return value

    def save(self, **kwargs):
        deposit_address = self.available_addresses.first()
        data = self.validated_data
        data["deposit_address"] = deposit_address
        return Order.objects.create(**data)


class CompleteOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['completed', ]

    def save(self, **kwargs):
        order = self.context["order"]
        order.completed = self.validated_data["completed"]
        order.save()


