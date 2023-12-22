from unittest import TestCase

from django.contrib.auth import get_user_model

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()


class AuthenticateTest(TestCase):
    """Тест: аутентификации"""

    def test_returns_None_if_no_such_token(self):
        """Тест: возвращается None, если нет такого маркера"""
        result = PasswordlessAuthenticationBackend().authenticate(
            "no-such-token"
        )
        self.assertIsNone(result)

    def test_retrurns_new_user_with_correct_email_if_token_exists(self):
        """Тест: возвращается новый пользователь с правильной электронной почтой, если маркер существует"""
        email = "jim9502@example.com"
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """Тест: возвращается существующий пользователь с правильной электронной почтой, если маркер существует"""
        email = "jim9502@example1.com"
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(user, existing_user)


class GetUserTest(TestCase):
    """Тест получения пользователя"""

    def test_gets_user_by_email(self):
        """Тест: получает пользователя по адресу электронной почты"""
        User.objects.create(email="john@example.com")
        desired_user = User.objects.create(email="jim9502@example2.com")
        found_user = PasswordlessAuthenticationBackend().get_user(
            "jim9502@example2.com"
        )
        self.assertEqual(found_user, desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        """Тест: возвращается None, если нет пользователя с таким адрисом электронной почты"""
        self.assertIsNone(
            PasswordlessAuthenticationBackend().get_user("wrong@example.com")
        )
