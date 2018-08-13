import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy

from cart.cart import Cart
from mixer.backend.django import mixer
from shop.tests.test_data import create_book_instance

from ..views import cart_add, cart_remove


class TestCartAddView(TestCase):
    def setUp(self):
        self.book = create_book_instance()
        self.req = RequestFactory().post(
            reverse_lazy("cart:cart_add", args=[self.book.id]))
        middleware = SessionMiddleware()
        middleware.process_request(self.req)
        self.req.session.save()

    def test_called_with_get_method(self):

        self.req = RequestFactory().get(
            reverse_lazy("cart:cart_add", args=[self.book.id]))

        resp = cart_add(self.req, self.book.id)
        self.assertEqual(resp.status_code, 405)

    def test_with_post_data(self):
        data = {'quantity': 1, 'update': False}
        self.req = RequestFactory().post(reverse_lazy(
            "cart:cart_add", args=[self.book.id]), data=data)
        middleware = SessionMiddleware()
        middleware.process_request(self.req)
        self.req.session.save()

        resp = cart_add(self.req, self.book.id)
        ct = Cart(self.req)
        self.assertEqual(len(ct), 1)

    def test_redirects_on_success(self):
        resp = cart_add(self.req, self.book.id)
        self.assertEqual(resp.status_code, 302)

    def test_raises_404_when_called_with_non_existent_book(self):
        with pytest.raises(Http404):
            cart_add(self.req, 2)


class TestCartRemoveView(TestCase):
    def setUp(self):
        self.book = create_book_instance()
        self.req = RequestFactory().post(
            reverse_lazy("cart:cart_remove", args=[self.book.id]))
        middleware = SessionMiddleware()
        middleware.process_request(self.req)
        self.req.session.save()

    def test_redirects_on_success(self):
        resp = cart_remove(self.req, self.book.id)
        self.assertEqual(resp.status_code, 302)

    def test_removed_item_from_cart(self):
        cart = Cart(self.req)
        resp = cart_remove(self.req, self.book.id)
        self.assertFalse(cart.cart)

    def test_raises_404_with_invalid_credentials(self):
        with pytest.raises(Http404):
            cart_remove(self.req, 2)


class TestCartDetailView(TestCase):
    def setUp(self):
        self.resp = self.client.get(reverse_lazy("cart:cart_detail"))

    def test_template_used(self):
        self.assertTemplateUsed(response=self.resp, template_name="cart/detail.html")
    
    def test_cart_in_context(self):
        self.assertIn('cart', self.resp.context)
    
    def test_profile_update_return_bool_for_auth_user(self):
        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        c.login(username='jacob', password='top_secret')
        self.resp = c.get(reverse_lazy("cart:cart_detail"))
        self.assertFalse(self.resp.context['profile_update'])


    def test_profile_update_return_none_for_unauth_user(self):
        
        self.resp = self.client.get(reverse_lazy("cart:cart_detail"))
        self.assertIsNone(self.resp.context['profile_update'])
        
