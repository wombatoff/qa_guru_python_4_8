
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart(product):
    cart = Cart()
    cart.add_product(product, 3)
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        assert product.check_quantity(500) is True
        assert product.check_quantity(1000) is True
        assert product.check_quantity(1500) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(10)
        assert product.quantity == 990

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(1100)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product(self, product, cart):
        cart.add_product(product, 2)
        assert cart.products[product] == 5

    def test_remove_product(self, product, cart):
        cart.remove_product(product, 2)
        assert cart.products[product] == 1

    def test_remove_product_without_quantity(self, product, cart):
        cart.remove_product(product)
        assert product not in cart.products

    def test_remove_product_with_greater_quantity(self, product, cart):
        cart.remove_product(product, 5)
        assert product not in cart.products

    def test_clear(self, cart):
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, product, cart):
        total_price = cart.get_total_price()
        assert total_price == 300

    def test_buy_success(self, product, cart):
        cart.buy()
        assert product.quantity == 997

    def test_buy_more_than_available(self, product, cart):
        cart.add_product(product, 2000)
        with pytest.raises(ValueError):
            cart.buy()
