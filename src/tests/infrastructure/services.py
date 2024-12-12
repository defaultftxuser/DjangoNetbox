from unittest import TestCase
from unittest.mock import MagicMock, patch
from django.db import IntegrityError

from src.infra.exceptions.repo_exceptions import UserAlreadyExistsException
from src.infra.services.users.user_service import UserService


class TestUserService(TestCase):
    def setUp(self):
        self.mock_user_repository = MagicMock()
        self.mock_token_repository = MagicMock()

        self.service = UserService(
            repository=self.mock_user_repository,
            token_repository=self.mock_token_repository
        )

    def test_create_user_success(self):
        mock_user = MagicMock()
        mock_saved_user = MagicMock()
        mock_token = "test_token"

        self.mock_user_repository.create.return_value = mock_user
        self.mock_user_repository.save.return_value = mock_saved_user
        self.mock_token_repository.get_or_create.return_value = (mock_token, True)

        result = self.service.create({"username": "test", "password": "1234"})

        self.mock_user_repository.create.assert_called_once_with(data={"username": "test", "password": "1234"})
        self.mock_user_repository.save.assert_called_once_with(instance=mock_user)
        self.mock_token_repository.get_or_create.assert_called_once_with(user=mock_saved_user)

        self.assertEqual(result, mock_token)

    def test_create_user_already_exists(self):
        self.mock_user_repository.create.side_effect = IntegrityError

        with self.assertRaises(UserAlreadyExistsException):
            self.service.create({"username": "existing_user", "password": "1234"})

        self.mock_user_repository.save.assert_not_called()
        self.mock_token_repository.get_or_create.assert_not_called()