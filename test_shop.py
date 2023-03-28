
import pytest

from models import Product, Cart


@pytest.fixture
def products():
    return [
        Product("book", 100, "This is a book", 1000),
        Product("phone", 200, "This is a phone", 500),
        Product("toy", 50, "This is a toy", 2000),
    ]


@pytest.fixture
def cart(products):
    cart = Cart()
    cart.add_product(products[0], 3)
    cart.add_product(products[1], 1)
    cart.add_product(products[2], 5)
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, products):

        assert products[0].check_quantity(500) is True
        assert products[0].check_quantity(1000) is True
        assert products[0].check_quantity(1001) is False
        assert products[1].check_quantity(500) is True
        assert products[2].check_quantity(2001) is False

    def test_product_buy(self, products):
        # TODO напишите проверки на метод buy
        products[0].buy(10)
        assert products[0].quantity == 990
        products[0].buy(990)
        assert products[0].quantity == 0

    def test_product_buy_more_than_available(self, products):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            products[0].buy(1100)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product(self, products, cart):
        cart.add_product(products[0], 2)
        assert cart.products[products[0]] == 5

    def test_remove_product(self, products, cart):
        cart.remove_product(products[0], 2)
        assert cart.products[products[0]] == 1

    def test_remove_product_without_quantity(self, products, cart):
        cart.remove_product(products[0])
        assert products[0] not in cart.products

    def test_remove_product_with_greater_quantity(self, products, cart):
        cart.remove_product(products[0], 3)
        assert products[0] not in cart.products

    def test_clear(self, cart):
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, products, cart):
        total_price = cart.get_total_price()
        assert total_price == 750
        cart.clear()
        assert cart.get_total_price() == 0

    def test_buy_success(self, products, cart):
        cart.buy()
        assert products[0].quantity == 997
        assert products[1].quantity == 499
        assert products[2].quantity == 1995

        cart.add_product(products[0], 997)
        cart.add_product(products[1], 499)
        cart.add_product(products[2], 1995)
        cart.buy()
        assert products[0].quantity == 0
        assert products[1].quantity == 0
        assert products[2].quantity == 0

    def test_buy_more_than_available(self, products, cart):
        cart.add_product(products[0], 2000)
        with pytest.raises(ValueError):
            cart.buy()

    def test_buy_insufficient_quantity_in_middle(self, products, cart):
        cart.add_product(products[0], 200)
        cart.add_product(products[1], 500)
        with pytest.raises(ValueError):
            cart.buy()
        assert products[0].quantity == 1000
        assert products[1].quantity == 500
        assert products[2].quantity == 2000
