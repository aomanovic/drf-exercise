from django.db.models import Q
from rest_framework.generics import get_object_or_404

from blockchain.models import Order, SearchAddress, UserAddresses
from blockchain.api.serializers import CompleteOrderSerializer, OrderSerializer, SearchAddressSerializer, \
    SearchTransactionSerializer, \
    UserAddressesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import requests


# TODO validate user requests using a 10sec pause
class SearchByAddressView(APIView):
    """
    Search By Address
    Required attributes:
    address - Bitcoin address can be base58 or hash160 max len=50
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, address, format=None):
        data = {"address": address, "user": request.user.id}
        # this api will only search for bitcoin addresses, so to add other currency addresses, their apis must be called
        url = f"https://blockchain.info/rawaddr/{address}"
        header = {'content-type': 'application/json'}
        res = requests.get(url=url, headers=header)
        if res.status_code == 200:
            serializer = SearchAddressSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            search_data = res.json()
            return Response(search_data, status=status.HTTP_200_OK)
        data['valid'] = False
        serializer = SearchAddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=status.HTTP_400_BAD_REQUEST)


# TODO validate user requests using a 10sec pause
class SearchByTransactionView(APIView):
    """
    Search By Transaction
    Required attributes:
    transaction - Transaction hex max len=64
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, transaction, format=None):
        data = {"transaction": transaction, "user": request.user.id}
        serializer = SearchTransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        url = f"https://blockchain.info/rawtx/{transaction}"
        header = {'content-type': 'application/json'}
        res = requests.get(url=url, headers=header)
        if res.status_code == 200:
            search_data = res.json()
            return Response(search_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSearchesView(APIView):
    """
    Past Searches
    Returns a list of all previous (past) searches made by the user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        search_addresses = SearchAddress.objects.filter(user=request.user.id)
        serializer = SearchAddressSerializer(search_addresses, many=True)
        return Response(serializer.data)


class UserAddressesView(APIView):
    """
    Address marking as mine
    You can mark an address as 'mine' using all previous (past) searches
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, address, user_id):
        try:
            return UserAddresses.objects.get(address=address, user=user_id)
        except UserAddresses.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        search_addresses = UserAddresses.objects.filter(user=request.user.id)
        serializer = UserAddressesSerializer(search_addresses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = {'user': request.user.id, 'address': request.data['address'], 'currency': request.data['currency']}
        serializer = UserAddressesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        address = self.get_object(address=request.data['address'], user_id=request.user.id)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserBalanceView(APIView):
    """
    Balance of all user addresses
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        addresses = [i.address for i in UserAddresses.objects.filter(user=request.user.id).all()]
        url = f"https://blockchain.info/balance?active={'|'.join(addresses)}"
        header = {'content-type': 'application/json'}
        res = requests.get(url=url, headers=header)
        if res.status_code == 200:
            data = res.json()
            agg_balance = sum([data[i]['final_balance'] for i in data])

            return Response({"balance": agg_balance}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class OrdersView(APIView):
    """
    Creating and listing Orders
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(deposit_address__user=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = {'amount': request.data['amount'], 'pair': request.data['pair'], 'side': request.data['side']}
        serializer = OrderSerializer(data=data, context={"user": request.user})
        if serializer.is_valid():
            created_order = serializer.save()
            return Response(OrderSerializer(created_order).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteOrderView(APIView):
    """
    Mark order as complete
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, deposit_address__user=request.user)
        serializer = CompleteOrderSerializer(data=request.data, context={"order": order})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)