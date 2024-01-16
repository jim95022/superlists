import os
import poplib
import time

from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from .base import FunctionalTest


SUBJECT = "Your login link for Superlists"


class LoginTest(FunctionalTest):
    """Тест регистрации в системе"""

    def test_can_get_email_link_to_log_in(self):
        """тест: можно получить ссылку по почте для регистрации"""

        # Олег заходит на сайт списков и впервые замечает раздел "войти" в навигационной панели.
        # Он говорит ему ввести свой адрес электронной почты, что Олег и делает
        if self.staging_server:
            test_email = "jim95022test@gmail.com"
        else:
            test_email = "jim9502@example.com"
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name("email").send_keys(test_email)
        self.browser.find_element_by_name("email").send_keys(Keys.ENTER)

        # Появляется сообщение, которое говорит, что ему на почту было выслано сообщение
        self.wait_for(lambda: self.assertIn(
            "Check your email",
            self.browser.find_element_by_tag_name("body").text
        ))

        # Олег проверят свою почту и находит сообщение
        body = self.wait_for_email(test_email, SUBJECT)

        # Письмо содержит ссылку на URL-адрес
        self.assertIn("Use this link to log in", body)
        url_search = re.search(r"http://.+/.+$", body)
        if not url_search:
            self.fail(f"Could not find url in email body:\n{body}")
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # Олег нажимает на ссылку
        self.browser.get(url)

        # Он зарегистрирован в системе!
        self.wait_to_be_logged_in(email=test_email)

        # Теперь он хочет выйти из системы
        self.browser.find_element_by_link_text("Log out").click()

        # Он вышел из системы
        self.wait_to_be_logged_out(email=test_email)

    def wait_for_email(self, test_email, subject):
        """Ожидать электронное сообщение"""
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL("pop.gmail.com")
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ.get("EMAIL_HOST_PASSWORD"))
            while time.time() - start < 60:
                # receive 10 new mails
                count, _ = inbox.stat()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print("getting msg", i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode("utf-8") for l in lines]
                    if f"Subject: {subject}" in lines:
                        email_id = i
                        body = "\n".join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

