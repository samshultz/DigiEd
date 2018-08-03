import datetime
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from mixer.backend.django import mixer
# from taggit.managers import TaggableManager

from ..models import Order, OrderItem
from shop.tests.test_data import create_book_instance


class TestOrderModel(TestCase):
    def test_can_create_order(self):
        order = mixer.blend(Order)
        self.assertEqual(Order.objects.count(), 1, "Should create Order")

    def test_str_representation(self):
        order = mixer.blend(Order)
        self.assertEqual(str(order), "Order 1")

    def test_transaction_ref_was_filled_in(self):
        order = mixer.blend(Order, tx_ref="")
        self.assertGreater(len(order.tx_ref), 1, "tx_ref should not be empty")

    def test_tx_ref_is_unique(self):
        with self.assertRaises(IntegrityError):
            order1 = mixer.blend(Order, tx_ref="fsdjk45yujk")
            order2 = mixer.blend(Order, tx_ref="fsdjk45yujk")

    def test_get_total_cost(self):
        order = mixer.blend(Order)
        book = create_book_instance()
        order_item1 = mixer.blend(
            OrderItem, order=order, book=book, quantity=1, price=2000)
        order_item2 = mixer.blend(
            OrderItem, order=order, book=book, quantity=1, price=2500)
        order_item3 = mixer.blend(
            OrderItem, order=order, book=book, quantity=1, price=1000)
        self.assertEqual(order.get_total_cost(),
                         sum([order_item1.get_cost(),
                              order_item2.get_cost(),
                              order_item3.get_cost()]))

    
class TestOrderItemModel(TestCase):
    def setUp(self):
        self.order = mixer.blend(Order)
        self.book = create_book_instance()

    def test_can_create_order_item(self):
        
        order_item1 = mixer.blend(
            OrderItem, order=self.order, book=self.book, quantity=1, price=2000)
        order_item2 = mixer.blend(
            OrderItem, order=self.order, book=self.book, quantity=1, price=2500)
        order_item3 = mixer.blend(
            OrderItem, order=self.order, book=self.book, quantity=1, price=1000)
        self.assertEqual(OrderItem.objects.count(), 3)
    
    def test_str_representation(self):
        
        order_item1 = mixer.blend(
            OrderItem, order=self.order, book=self.book, quantity=1, price=2000)
        self.assertEqual(str(order_item1), str(order_item1.pk))
    
    def test_get_cost(self):
        
        order_item1 = mixer.blend(
            OrderItem, order=self.order, book=self.book, quantity=1, price=2000)
        self.assertEqual(order_item1.get_cost(), 2000)
    
    def test_negative_prices(self):
        with self.assertRaisesMessage(ValidationError, "Prices can't be negative"):
            order_item1 = mixer.blend(
                OrderItem, order=self.order, book=self.book, quantity=1, price=-2000)
    
    def test_negative_quantity(self):
        with self.assertRaisesMessage(ValidationError, "Quantity can't be negative"):
            order_item1 = mixer.blend(
                OrderItem, order=self.order, book=self.book, quantity=-1, price=2000)
                
