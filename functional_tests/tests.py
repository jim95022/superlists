import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
    """Тест нового посетителя"""


    def setUp(self):
        """Установка"""
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get("STAGING_SERVER")
        if staging_server:
            self.live_server_url = "http://" + staging_server


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


    def test_can_start_a_list_for_one_user(self):
        """Тест: можно начать список для одного пользователя"""

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


        # Олег закрывает браузер и идет в магазин.
        self.browser.quit()



    def test_multiple_users_can_start_lists_at_different_urls(self):
        """Тест: многочисленные пользователи могут начать списки по разным url"""
        
        # Олег начинает новый список
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Купить молока")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Купить молока")


        # Олегу интересно останится ли запись после того как он закроет сайт. 
        # Он обращает внимание что сайт сгенерировал уникальный URL адрес. 
        # Также присутсует небольшой текст с объснением
        oleg_list_url = self.browser.current_url
        self.assertRegex(oleg_list_url, r"/lists/.+")


        # Теперь приходит новый пользователь, Руслан

        ## Мы создаем новый сеанс браузера, чтобы обеспечить изолированность.
        ## Никакая инофрмация от Олега не должна остаться. Включая куки и тд.
        self.browser.quit()
        self.browser = webdriver.Firefox()


        # Руслан открывает домашнюю страницу. Нет никаких признаков списка Олега.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Купить молока", page_text)
        self.assertNotIn("Cмешать молоко и бананаы в блендере", page_text)


        # Руслан начинает свой список. вводня новый элемент.
        inputbox = self.browser.find_element_by_id("id_new_item")
        inputbox.send_keys("Заказать протеин")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Заказать протеин")


        # Руслан получает уникальный URL адрес
        ruslan_list_url = self.browser.current_url
        self.assertRegex(ruslan_list_url, r"/lists/.+")
        self.assertNotEqual(ruslan_list_url, oleg_list_url)


        # Опять таки нет следа от Олега
        page_text = self.browser.find_element_by_tag_name("body").text
        self.assertNotIn("Купить молока", page_text)
        self.assertNotIn("Cмешать молоко и бананаы в блендере", page_text)


        # Оба закрывают странцу и ложаться спать.

    def test_layout_and_styling(self):
        """Тест макета и стилевого оформления"""
        # Олег открывает домашнюю страницу
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Олег замечает, что поле ввода аккуратно центрировано
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )

        # Олег начинает новый список и видит, что поле ввода тм тоже
        # Аккуратно центировано
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. testing")
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=10
        )
