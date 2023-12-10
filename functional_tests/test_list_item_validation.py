from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """Тест валидации элемента списка"""

    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        # Олег открывает домашнюю страницу и случайно пытается отправить пустой элемент списка.
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # Домашняя страница обновляется, и появляется сообщение об ошибке, которое говорит,
        # что элементы списка не должны быть пустми.
        self.wait_for(
            lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,
            "You can't have an empty list item"
            )
        )

        # Он пробует снова, теперь с некми текстом для элемента, и теперь срабатывает
        self.browser.find_element_by_id("id_new_item").send_keys("Buy milk")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy milk")

        # Как ни странно, Олег решает отправить второй пустой список элемента
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)

        # Он получает аналогичное предупреждение на странице списка
        self.wait_for(
            lambda: self.assertEqual(
            self.browser.find_element_by_css_selector(".has-error").text,
            "You can't have an empty list item"
            )
        )

        # И он может его исправить, заполнив поле неким текстом
        self.browser.find_element_by_id("id_new_item").send_keys("Make tea")
        self.browser.find_element_by_id("id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy milk")
        self.wait_for_row_in_list_table("2. Make tea")
