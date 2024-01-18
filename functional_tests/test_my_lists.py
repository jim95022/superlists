from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from .server_tools import create_session_on_server
from functional_tests.base import FunctionalTest
from functional_tests.management.commands.create_session import create_pre_authenticated_session

User = get_user_model()


class MyListsTest(FunctionalTest):
    """Тест приложения 'Мои списки'"""

    def create_pre_authenticated_session(self, email):
        '''Создать предварительно аутентифицированный сеанс'''
        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        # Установить cookie, которые нужны для первого посещения домена.
        # Страницы 404 загружаются быстрее всего!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session_key,
                path="/",
            )
        )

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        """Тест: списки зарегистрированных пользователей сохраняются как 'мои списки'"""
        email = "jim@gmail.com"

        # Олег является зарегестрированным пользователем
        self.create_pre_authenticated_session(email)

        # Олег открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_list_item("Reticulate splines")
        self.add_list_item("Immanentize eschaton")
        first_list_url = self.browser.current_url

        # Он замечает ссылку на "Мои списки" в первый раз
        self.browser.find_element_by_link_text("My lists").click()

        # Она видит, что ее список находится там, и он назван на основе первого элемента списка
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Reticulate splines")
        )
        self.browser.find_element_by_link_text("Reticulate splines").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Он решает начать еще один список, чтобы только убедиться
        self.browser.get(self.live_server_url)
        self.add_list_item("Click cows")
        second_list_url = self.browser.current_url

        # Под заголовком "Мои списки" появляется ее новый список
        self.browser.find_element_by_link_text("My lists").click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text("Click cows")
        )

        self.browser.find_element_by_link_text("Click cows").click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Она выходит из системы. Опция "Мои списки" исчезает
        self.browser.find_element_by_link_text("Log out").click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements_by_link_text("My lists"),
                []
            )
        )
