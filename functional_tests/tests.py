from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    """Тест нового посетителя"""

    def setUp(self):
        """Установка"""
        self.browser = webdriver.Firefox()

    def tearDown(self):
        """Демонтаж"""
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """Ожидать строку в таблице списка"""
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id("id_list_table")
                rows = table.find_elements_by_tag_name("tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(1/2)

    def test_can_start_a_list_and_retrieve_it_later(self):
        """Тест: можно начать новый список и получить его позже"""

        # Олег узнал про новое приложение для списков дел.
        # Ему кмдают ссылку и он переходит на домашнюю страницу.
        self.browser.get(self.live_server_url)


        # Он обращает внимение что заголовок страницы говорят о туду списке
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name("h1").text
        self.assertIn("To-Do", header_text)


        # Олегу предлагается ввести элемент списка
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertEqual(
            inputbox.get_attribute("placeholder"),
            "Enter a to-do item"
        )


        # Олежа набирает в текстовом поле "Купить молока". (Олег готовит привосходные молочные коктейли)
        inputbox.send_keys("Купить молока")


        # Олег нажимает Enter, страница обновляется, и теперь страница содержит первый элемент "1. Купить молока"
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Купить молока")


        # Текстовое поле по-прежнему приглашает его добавить еще одно поле. Олег вводит "смешать молоко и бананаы в блендере"
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Cмешать молоко и бананаы в блендере")
        inputbox.send_keys(Keys.ENTER)


        # Страница обновляется и теперь отображается два элемента в списке. 
        self.wait_for_row_in_list_table("1. Купить молока")
        self.wait_for_row_in_list_table("2. Cмешать молоко и бананаы в блендере")


        # Олегу интересно останится ли запись после того как он закроет сайт. 
        # Он обращает внимание что сайт сгенерировал уникальный URL адрес. 
        # Также присутсует небольшой текст с объснением
        self.fail("Закончить тест!")


        # Олег снова посещает этот уникальный URL адрес, список по прежнему там.


        # Олег закрывает браузер и идет в магазин.
        self.browser.quit()
