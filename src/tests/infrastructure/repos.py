from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models import Q

from src.infra.repos.devices.devices_repos import DeviceRepository, DeviceModelRepository
from src.infra.repos.users.users_repo import UserRepository, TokenRepository
from src.presentation.apps.device_app.models import DeviceModel, Device


class UserRepositoryTest(TestCase):
    def setUp(self):
        self.repository = UserRepository()

    def test_create_user(self):
        data = {"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}
        user = self.repository.create(data)
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_get_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        fetched_user = self.repository.get(Q(username="testuser"))
        self.assertEqual(fetched_user, user)

    def test_get_by_pk(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        fetched_user = self.repository.get_by_pk(user.pk)
        self.assertEqual(fetched_user, user)

    def test_filter_users(self):
        User.objects.create_user(username="user1", email="user1@example.com", password="password1")
        User.objects.create_user(username="user2", email="user2@example.com", password="password2")
        users = self.repository.filter(Q(email__contains="example.com"))
        self.assertEqual(users.count(), 2)

    def test_update_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        updated_user = self.repository.update(user.pk, {"email": "newemail@example.com"})
        self.assertEqual(updated_user.email, "newemail@example.com")

    def test_delete_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        self.repository.delete(Q(username="testuser"))
        self.assertFalse(User.objects.filter(username="testuser").exists())


class TokenRepositoryTest(TestCase):
    def setUp(self):
        self.repository = TokenRepository()

    def test_get_or_create_token(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        token, created = self.repository.get_or_create(user=user)
        self.assertTrue(created)
        self.assertTrue(token.key)
        self.assertEqual(token.user, user)

    def test_get_token(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        token = Token.objects.create(user=user)
        fetched_token = self.repository.get(Q(user=user))
        self.assertEqual(fetched_token, token)

    def test_delete_token(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword")
        Token.objects.create(user=user)
        self.repository.delete(Q(user=user))
        self.assertFalse(Token.objects.filter(user=user).exists())


class TestUserRepositoryNegative(TestCase):
    def setUp(self):
        self.user_repo = UserRepository()

    @patch("src.infra.repos.users.users_repo.UserRepository.create")
    def test_create_user_invalid_data(self, mock_create_user):
        mock_create_user.side_effect = ValueError("Invalid data")
        with self.assertRaises(ValueError):
            self.user_repo.create({"username": "", "password": ""})
        mock_create_user.assert_called_once()

    @patch("src.infra.repos.users.users_repo.UserRepository.get")
    def test_get_nonexistent_user(self, mock_get):
        mock_get.return_value = None

        result = self.user_repo.get(Q(username="test_mock_user"))

        self.assertIsNone(result)
        mock_get.assert_called_once_with(Q(username="test_mock_user"))

    @patch("src.infra.repos.users.users_repo.UserRepository.filter")
    def test_filter_no_results(self, mock_filter):
        mock_filter.return_value = []
        result = self.user_repo.filter(Q(username="nonexistent"))
        self.assertEqual(result, [])
        mock_filter.assert_called_once_with(Q(username="nonexistent"))


class TestTokenRepositoryNegative(TestCase):
    def setUp(self):
        self.token_repo = TokenRepository()

    @patch("rest_framework.authtoken.models.Token.objects.get_or_create")
    def test_create_token_for_invalid_user(self, mock_get_or_create):
        mock_get_or_create.side_effect = ValueError("Invalid user")
        invalid_user = None
        with self.assertRaises(ValueError):
            self.token_repo.get_or_create(invalid_user)
        mock_get_or_create.assert_called_once_with(user=invalid_user)

    @patch("rest_framework.authtoken.models.Token.objects.get")
    def test_get_nonexistent_token(self, mock_get):
        mock_get.return_value = None
        result = self.token_repo.get(Q(key="invalid_key"))
        self.assertIsNone(result)
        mock_get.assert_called_once_with(Q(key="invalid_key"))

    @patch("rest_framework.authtoken.models.Token.objects.filter")
    def test_delete_nonexistent_token(self, mock_filter):
        mock_filter.return_value.delete.return_value = (0, {})

        result = self.token_repo.delete(Q(user_id=999))

        self.assertEqual(result, (0, {}))


class TestDeviceRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="testuser", password="password")
        cls.device_model = DeviceModel.objects.create(name="Model 1", description="Test model")
        cls.repository = DeviceRepository()

    def test_create_device(self):
        data = {
            "name": "Device 1",
            "ip_address": "192.168.0.1",
            "address": "123 Test St.",
            "author": self.user,
            "device_model": self.device_model,
            "comment": "This is a test device",
        }

        device = self.repository.create(data=data)
        self.assertEqual(device.name, "Device 1")
        self.assertEqual(device.ip_address, "192.168.0.1")
        self.assertEqual(device.address, "123 Test St.")
        self.assertEqual(device.author, self.user)
        self.assertEqual(device.device_model, self.device_model)
        self.assertEqual(device.comment, "This is a test device")

    def test_filter_device(self):
        Device.objects.create(
            name="Device 1",
            ip_address="192.168.0.1",
            address="123 Test St.",
            author=self.user,
            device_model=self.device_model,
        )
        Device.objects.create(
            name="Device 2",
            ip_address="192.168.0.2",
            address="456 Test St.",
            author=self.user,
            device_model=self.device_model,
        )

        devices = self.repository.filter(Q(name="Device 1"))
        self.assertEqual(devices.count(), 1)
        self.assertEqual(devices.first().ip_address, "192.168.0.1")

    def test_delete_device(self):
        device = Device.objects.create(
            name="Device 1",
            ip_address="192.168.0.1",
            address="123 Test St.",
            author=self.user,
            device_model=self.device_model,
        )

        self.repository.delete(Q(pk=device.pk))
        self.assertFalse(Device.objects.filter(pk=device.pk).exists())


class TestDeviceModelRepository(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.repository = DeviceModelRepository()

    def test_create_device_model(self):
        data = {"name": "Model 1", "description": "Test model"}
        device_model = self.repository.create(data=data)
        self.assertEqual(device_model.name, "Model 1")
        self.assertEqual(device_model.description, "Test model")

    def test_get_device_model(self):
        device_model = DeviceModel.objects.create(name="Model 1", description="Test model")
        result = self.repository.get(Q(pk=device_model.pk))
        self.assertEqual(result, device_model)

    def test_update_device_model(self):
        device_model = DeviceModel.objects.create(name="Model 1", description="Test model")
        updated_data = {"name": "Updated Model", "description": "Updated description"}
        updated_device_model = self.repository.update(pk=device_model.pk, data=updated_data)
        self.assertEqual(updated_device_model.name, "Updated Model")
        self.assertEqual(updated_device_model.description, "Updated description")
