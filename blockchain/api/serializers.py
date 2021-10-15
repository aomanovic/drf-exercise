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
        fields = ['user', 'address']
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
        fields = ['id', 'amount', 'deposit_address', 'completed']
        read_only_fields = ['id', 'deposit_address', 'completed']

    def validate(self, value):
        user = self.context["user"]
        user_addresses = get_available_addresses(user)

        if not user_addresses.exists():
            raise serializers.ValidationError("There are no available addresses")

        return value

    def save(self, **kwargs):
        user = self.context["user"]
        deposit_address = get_available_addresses(user).first()
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


