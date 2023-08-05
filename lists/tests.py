from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page


class HomePageTest(TestCase):
    """Тест на домашней страницы"""

    def test_root_url_resolves_to_home_page_view(self):
        """Тест: корневой URL преобразуется в предоставление домашней страницы"""
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """Тест: домашняя страница возвращает правильный html"""
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8")
        
        self.assertTrue(html.startswith("<html>"))
        self.assertIn("<title>To-Do lists</title>", html)
        self.assertTrue(html.endswith("</html>"))