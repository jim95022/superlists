from functional_tests.base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    """Тест валидации элемента списка"""

    def test_connot_add_empty_list_items(self):
        """Тест: нельзя добавлять пустые элементы списка"""
        # Олег открывает домашнюю страницу и случайно пытается отправить пустой элемент списка.

        # Домашняя страница обновляется, и появляется сообщение об ошибке, которое говорит,
        # что элементы списка не должны быть пустми.

        # Он пробует снова, теперь с некми текстом для элемента, и теперь срабатывает

        # Как ни странно, Олег решает отправить второй пустой список элемента

        # Он получает аналогичное предупреждение на странице списка

        # И он может его исправить, заполнив поле неким текстом
        self.fail("Напиши Меня!")
