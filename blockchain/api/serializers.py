from rest_framework import serializers
from blockchain.models import SearchAddress, SearchTransaction, UserAddresses
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

