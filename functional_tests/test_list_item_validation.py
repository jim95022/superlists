from selenium.webdriver.common.keys import Keys

from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """Тест валидации элемента списка"""

    def test_cannot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        # Олег открывает домашнюю страницу и случайно пытается отправить пустой элемент списка.
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_element_by_css_selector("#id_text:invalid"))

        # Олег начинает набирать текст нового элемента и ошибка исчезает
        self.get_item_input_box().send_keys("Buy milk")
        self.wait_for(lambda: self.browser.find_element_by_css_selector("#id_text:valid"))

        # Он теперь может отправить его успешно
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy milk")

        # Как ни странно, Олег решает отправить второй пустой список элемента
        self.get_item_input_box().send_keys(Keys.ENTER)

        # и снова браузер не подчинился
        self.wait_for_row_in_list_table("1. Buy milk")
        self.wait_for(lambda: self.browser.find_element_by_css_selector("#id_text:invalid"))

        # И он может его исправить, заполнив поле неким текстом
        self.get_item_input_box().send_keys("Make tea")
        self.wait_for(lambda: self.browser.find_element_by_css_selector("#id_text:valid"))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy milk")
        self.wait_for_row_in_list_table("2. Make tea")
    
    def test_cannot_add_duplicate_items(self):
        """Тест: нельзя добавлять повторяющиеся элементы"""
        # Олег открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Buy wellies")

        # Он случайно пытается ввести элемент повторно
        self.get_item_input_box().send_keys("Buy wellies")
        self.get_item_input_box().send_keys(Keys.ENTER)

        # Он видит полезное сообщение об ошибке
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_element_by_css_selector(".has-error").text,
                "You've already got this in your list"
            )
        )
