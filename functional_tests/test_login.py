from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest


TEST_EMAIL = "jim9502@example.com"
SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    """Тест регистрации в системе"""

    def test_can_get_email_link_to_log_in(self):
        """тест: можно получить ссылку по почте для регистрации"""

        # Олег заходит на сайт списков и впервые замечает раздел "войти" в навигационной панели.
        # Он говорит ему ввести свой адрес электронной почты, что Олег и делает
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(TEST_EMAIL)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ему на почту было выслано сообщение
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name("body").text
        ))

        # Олег проверят свою почту и находит сообщение
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # Письмо содержит ссылку на URL-адрес
        self.assertIn("Use this link to log in", email.body)
        url_search = re.search(r"http://.+/.+$", email.body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{email.body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Олег нажимает на ссылку
        self.browser.get(url)

        # Он зарегистрирован в системе!
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Log out")
        )
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn(TEST_EMAIL, navbar.text)
