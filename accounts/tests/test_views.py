from django.test import TestCase
from unittest.mock import patch, call
import accounts.views
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):
    """Тест представления, которое отправляет сообщения для входа в систему"""

    def test_redirects_to_home_page(self):
        """Тест: переадресуется на домашнюю страницу"""
        response = self.client.get("/accounts/login?token=abcd123")
        self.assertRedirects(response, "/")

    @patch("accounts.views.send_mail")
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        """Тест: отправляется сообщение на адрес из метода post"""

        self.client.post("/accounts/send_login_email", data={
            "email": "jim9502@example.com"
        })

        self.assertTrue(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertEqual(subject, "Your login link for Superlists")
        self.assertEqual(from_email, "noreply@superlists")
        self.assertEqual(to_list, ["jim9502@example.com"])

    def test_adds_success_message(self):
        """Тест: добавляется сообщение об успехе"""
        response = self.client.post(
            "/accounts/send_login_email",
            data={
                "email": "jim9502@exaple.com"
            },
            follow=True
        )

        message = list(response.context["messages"])[0]
        self.assertEqual(
            message.message,
            "Check your email",
        )
        self.assertEqual(message.tags, "success")

    def test_creates_token_associated_with_email(self):
        """Тест: создается маркер, связанный с электронной почтой"""
        self.client.post("/accounts/send_login_email", data={
            "email": "jim9502@example.com"
        })
        token = Token.objects.first()
        self.assertEqual(token.email, "jim9502@example.com")

    @patch("accounts.views.send_mail")
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """Тест: отсылается ссылка на вход в систему, используя uid маркера"""
        self.client.post(
            "/accounts/send_login_email",
            data={
                "email": "jim9502@gmail.com"
            }
        )

        token = Token.objects.first()
        expected_url = f"http://testserver/accounts/login?token={token.uid}"
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

    @patch("accounts.views.auth")
    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        """Тест: вызывается authenticate c uid из GET-запроса"""
        self.client.get("/accounts/login?token=abcd123")
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid="abcd123")
        )
