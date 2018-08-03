import pytest
from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy
from shop.models import Category
from cart.cart import Cart
from mixer.backend.django import mixer
from shop.tests.test_data import create_book_instance


class TestCart(TestCase):
    def setUp(self):
        self.req = RequestFactory().get("/")
        middleware = SessionMiddleware()
        middleware.process_request(self.req)
        self.req.session.save()
    def test_can_initialize_cart(self):
        
        cart = Cart(self.req)
        self.assertFalse(cart.cart)
    
    def test_can_add_one_item_to_cart(self):
        
        cart = Cart(self.req)
        
        book = create_book_instance()
        cart.add(book)
        self.assertEqual(len(cart), 1)
        self.assertIn(str(book.id), cart.cart.keys())

    def test_can_add_multiple_items_to_cart(self):
        cart = Cart(self.req)
        
        cat1 = mixer.blend(Category)
        book1 = create_book_instance()
        book2 = create_book_instance(category=cat1)
        cart.add(book1)
        cart.add(book2)
        self.assertEqual(len(cart), 2)
        self.assertIn(str(book1.id), cart.cart.keys())
        self.assertIn(str(book2.id), cart.cart.keys())
    
    def test_can_remove_item_form_cart(self):
        cart = Cart(self.req)
        
        cat1 = mixer.blend(Category)
        book1 = create_book_instance()
        book2 = create_book_instance(category=cat1)
        cart.add(book1)
        cart.add(book2)
        cart.remove(book1)
        self.assertEqual(len(cart), 1)
        self.assertNotIn(str(book1.id), cart.cart.keys())
    
    def test_get_total_price_with_single_qty(self):
        cart = Cart(self.req)
        
        cat1 = mixer.blend(Category)
        book1 = create_book_instance()
        book2 = create_book_instance(category=cat1)
        cart.add(book1)
        cart.add(book2)
        
        self.assertEqual(cart.get_total_price(), sum([book1.price, book2.price]))
    
    def test_can_clear_cart(self):
        cart = Cart(self.req)
        
        cat1 = mixer.blend(Category)
        book1 = create_book_instance()
        book2 = create_book_instance(category=cat1)
        cart.add(book1, 3)
        cart.add(book2, 2)
        cart.clear()

        with pytest.raises(KeyError):
            self.assertFalse(cart.session[settings.CART_SESSION_ID])
    
    def test_get_total_price_with_featured_item(self):
        cart = Cart(self.req)
        
        cat1 = mixer.blend(Category)
        book1 = create_book_instance()
        book2 = create_book_instance(category=cat1, featured=True, discount_price=500)
        cart.add(book1)
        cart.add(book2)
        self.assertEqual(cart.get_total_price(), sum([book1.price, book2.discount_price]))