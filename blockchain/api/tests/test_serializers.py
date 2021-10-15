from blockchain.api.serializers import CompleteOrderSerializer, OrderSerializer, SearchAddressSerializer, \
    SearchTransactionSerializer, \
    UserAddressesSerializer
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


class TestSearchAddressSerializer(APITestCase):
    def setUp(self):
        data = {'username': 'testLogin', "password": "testPassword.1"}
        _ = self.client.post(path=reverse("accounts:reg_view"), data=data)

    def test_normal_serialization_validation(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = SearchAddressSerializer(data=data)
        self.assertTrue(ser.is_valid())

    def test_serialization_validation_without_address(self):
        data = {'user': 1}
        ser = SearchAddressSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_user(self):
        data = {'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = SearchAddressSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_any_data(self):
        data = {}
        ser = SearchAddressSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_create_with_valid_field(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d', 'vadlid': False}
        ser = SearchAddressSerializer(data=data)
        ser.is_valid()
        ser.save()
        self.assertEqual(ser.data.keys(), {"timestamp", "user", "address", "valid"})

    def test_serialization_create_without_valid_field(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = SearchAddressSerializer(data=data)
        ser.is_valid()
        ser.save()
        self.assertEqual(ser.data.keys(), {"timestamp", "user", "address", "valid"})


class TestSearchTransactionSerializer(APITestCase):
    def setUp(self):
        data = {'username': 'testLogin', "password": "testPassword.1"}
        _ = self.client.post(path=reverse("accounts:reg_view"), data=data)

    def test_normal_serialization_validation(self):
        data = {'user': 1, 'transaction': 'adsadasdgsdf564f63d4f3241d'}
        ser = SearchTransactionSerializer(data=data)
        self.assertTrue(ser.is_valid())

    def test_serialization_validation_without_address(self):
        data = {'user': 1}
        ser = SearchTransactionSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_user(self):
        data = {'transaction': 'adsadasdgsdf564f63d4f3241d'}
        ser = SearchTransactionSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_any_data(self):
        data = {}
        ser = SearchTransactionSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_create(self):
        data = {'user': 1, 'transaction': 'adsadasdgsdf564f63d4f3241d'}
        ser = SearchTransactionSerializer(data=data)
        ser.is_valid()
        ser.save()
        self.assertEqual(ser.data.keys(), {"user", "transaction"})


class TestUserAddressesSerializer(APITestCase):
    def setUp(self):
        data = {'username': 'testLogin', "password": "testPassword.1"}
        _ = self.client.post(path=reverse("accounts:reg_view"), data=data)
        ser = SearchAddressSerializer(data={'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'})
        ser.is_valid()
        ser.save()

    def test_normal_serialization_validation(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = UserAddressesSerializer(data=data)
        self.assertTrue(ser.is_valid())

    def test_serialization_validation_without_address(self):
        data = {'user': 1}
        ser = UserAddressesSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_user(self):
        data = {'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = UserAddressesSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_validation_without_any_data(self):
        data = {}
        ser = UserAddressesSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_create(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = UserAddressesSerializer(data=data)
        ser.is_valid()
        ser.save()
        self.assertEqual(ser.data.keys(), {"user", "address"})

    def test_serialization_not_searched_address(self):
        data = {'user': 1, 'address': 'sdgsdf564f63d4f3241d'}
        ser = UserAddressesSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertEqual(ser.errors.keys(), {"non_field_errors"})

    def test_serialization_dublicate_address_save(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = UserAddressesSerializer(data=data)
        ser.is_valid()
        ser.save()
        ser = UserAddressesSerializer(data=data)
        self.assertFalse(ser.is_valid())
        self.assertEqual(ser.errors.keys(), {"non_field_errors"})


class TestCompleteOrderSerializer(APITestCase):
    def setUp(self):
        data = {'username': 'testLogin', "password": "testPassword.1"}
        _ = self.client.post(path=reverse("accounts:reg_view"), data=data)

    def test_serialization_complete_order_invalid(self):
        data = {'completed': 'abcd'}
        ser = CompleteOrderSerializer(data=data)
        self.assertFalse(ser.is_valid())

    def test_serialization_complete_order_valid(self):
        data = {'completed': True}
        ser = CompleteOrderSerializer(data=data)
        self.assertTrue(ser.is_valid())


class TestOrderSerializer(APITestCase):
    def setUp(self):
        data = {'username': 'testLogin', "password": "testPassword.1"}
        _ = self.client.post(path=reverse("accounts:reg_view"), data=data)
        ser = SearchAddressSerializer(data={'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'})
        ser.is_valid()
        ser.save()

    def test_serialization_create_order_address_not_set(self):
        data = {'amount': 123.00}
        ser = OrderSerializer(data=data, context={"user": 1})
        self.assertFalse(ser.is_valid())
        self.assertEqual(ser.errors.keys(), {"non_field_errors"})

    def test_serialization_create_order_invalid_input(self):
        data = {'amount': "abc"}
        ser = OrderSerializer(data=data, context={"user": 1})
        self.assertFalse(ser.is_valid())

    def test_serialization_create_order(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = UserAddressesSerializer(data=data)
        ser.is_valid()
        ser.save()

        data = {'amount': 123.00}
        ser = OrderSerializer(data=data, context={"user": 1})
        ser.is_valid()
        created_object = ser.save()
        self.assertIsNotNone(created_object.id)
        self.assertEqual(created_object.amount, data["amount"])

    def test_serialization_create_order_no_available_address(self):
        data = {'user': 1, 'address': 'adsadasdgsdf564f63d4f3241d'}
        ser = UserAddressesSerializer(data=data)
        ser.is_valid()
        ser.save()

        data = {'amount': 123.00}
        ser = OrderSerializer(data=data, context={"user": 1})
        ser.is_valid()
        ser.save()

        ser = OrderSerializer(data=data, context={"user": 1})
        self.assertFalse(ser.is_valid())
        self.assertEqual(ser.errors.keys(), {"non_field_errors"})
        self.assertEqual(ser.errors['non_field_errors'][0], "There are no available addresses")
