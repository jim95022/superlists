from django.http import HttpRequest
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page
from lists.models import Item


class HomePageTest(TestCase):
    """Тест на домашней страницы"""

    def test_root_url_resolves_to_home_page_view(self):
        """Тест: корневой URL преобразуется в предоставление домашней страницы"""
        found = resolve("/")
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        """Тест: домашняя страница возвращает правильный html"""
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_can_save_a_POST_request(self):
        """Тест: можно сохранить post-запрос"""
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertIn("a new list item", response.content.decode())
        self.assertTemplateUsed(response, "home.html")


class ItemModelTest(TestCase):
    """Тест модели элемента списка"""

    def test_saving_and_retrieving_items(self):
        """Тест сохранения и получения элементов списка"""
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")
