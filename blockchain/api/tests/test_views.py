from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
import json
import time
from blockchain.api.serializers import SearchAddressSerializer


class TestSearchByAddressView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("blockchain_api:search_address", kwargs={'address': "1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F"})

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_search_address_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        time.sleep(10)

    def test_search_not_existing_address(self):
        response = self.client.get(reverse("blockchain_api:search_address", kwargs={'address': "test123"}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        time.sleep(10)

    def test_search_address_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestSearchByTransactionView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("blockchain_api:search_transaction",
                           kwargs={'transaction': "129efb63b30b8a275691b6e24904022f5a6299705afe2816b05752bf3559a0e9"})

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_search_transaction_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        time.sleep(10)

    def test_search_not_existing_transaction(self):
        response = self.client.get(reverse("blockchain_api:search_transaction", kwargs={'transaction': "test123"}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        time.sleep(10)

    def test_search_transaction_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserSearchesView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("blockchain_api:past_searches")
        self.client.get(
            reverse("blockchain_api:search_address", kwargs={'address': "1A8JiWcwvpY7tAopUkSnGuEYHmzGYfZPiq"}))
        time.sleep(10)

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_searches_authenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_searches_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserAddressesView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("blockchain_api:mine_addresses")
        ser = SearchAddressSerializer(data={"address": "1BoatSLRHtKNngkdXEeobR76b53LETtpyT", "user": 1})
        ser.is_valid()
        ser.save()

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_marked_as_mine(self):
        data = {"address": "1BoatSLRHtKNngkdXEeobR76b53LETtpyT", "currency": "BTC"}
        self.client.post(self.url, data=data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_marked_as_mine_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_address_as_mine(self):
        data = {"address": "1BoatSLRHtKNngkdXEeobR76b53LETtpyT", "currency": "BTC"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_unsearched_address_as_mine(self):
        data = {"address": "dasdfdsf", "currency": "BTC"}
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mark_searched_invalid_address_as_mine(self):
        data = {"address": "ttt123", "currency": "BTC"}
        ser = SearchAddressSerializer(data={"address": "ttt123", "user": 1, "valid": False})
        ser.is_valid()
        ser.save()
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unmark_searched_address_as_mine(self):
        data = {"address": "1BoatSLRHtKNngkdXEeobR76b53LETtpyT", "currency": "BTC"}
        ser = SearchAddressSerializer(data={"address": "1BoatSLRHtKNngkdXEeobR76b53LETtpyT", "user": 1})
        ser.is_valid()
        ser.save()
        self.client.post(self.url, data=data)
        response = self.client.delete(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestUserBalanceView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password="passwordTesting.123")
        self.token = Token.objects.create(user=self.user)
        self.api_auth()
        self.url = reverse("blockchain_api:balance")

    def api_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_balance_authenticated(self):
        ser = SearchAddressSerializer(data={"address": "1A8JiWcwvpY7tAopUkSnGuEYHmzGYfZPiq", "user": 1})
        ser.is_valid()
        ser.save()
        ser = SearchAddressSerializer(data={"address": "1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F", "user": 1})
        ser.is_valid()
        ser.save()
        self.client.post(reverse("blockchain_api:mine_addresses"),
                         data={'address': "1A8JiWcwvpY7tAopUkSnGuEYHmzGYfZPiq", "currency": "BTC"})
        self.client.post(reverse("blockchain_api:mine_addresses"),
                         data={'address': "1AJbsFZ64EpEfS5UAjAfcUG8pH8Jn3rn1F", "currency": "BTC"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(json.loads(response.content)['balance'], 0)

    def test_balance_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
