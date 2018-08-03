from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy
import pytest
from django.http import Http404
from mock import patch

from cart.cart import Cart
from mixer.backend.django import mixer
from shop.tests.test_data import create_book_instance

from ..models import Order, OrderItem
from ..views import confirm_payment, order_create, order_list, order_detail


class TestOrderCreateView(TestCase):
    def test_post_request(self):
        data = {"first_name": "Sam", 'last_name': "James",
                "email": "admin@mail.com"}
        req = RequestFactory().post(reverse_lazy("orders:order_create"), data=data)
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()
        # create a book instance and add it to cart
        book = create_book_instance()
        ct = Cart(req)
        ct.add(book)

        resp = order_create(req)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_get_request(self):
        resp = self.client.get(reverse_lazy("orders:order_create"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(
            response=resp, template_name="orders/order/create.html")
        self.assertIn("form", resp.context)


class TestConfirmPaymentView(TestCase):
    @patch("orders.views.Paystack")
    def test_payment(self, mock_Paystack):
        order = mixer.blend(Order)
        req = RequestFactory().post(reverse_lazy(
            "orders:download", args=[order.id]))
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()
        # create a book instance and add it to cart
        book = create_book_instance()
        ct = Cart(req)
        ct.add(book)
        mock_Paystack(secret_key=settings.PAYSTACK_SECRET_KEY).transaction.verify(reference=order.tx_ref).return_value = {
            'data': {'status': 'success', 'amount': ct.get_total_price()}}
        resp = confirm_payment(req, order.id)

        self.assertEqual(resp.status_code, 200)


class TestOrderDetailView(TestCase):
    def test_raises_404_when_called_with_invalid_arguments(self):
        req = RequestFactory().get(reverse_lazy("orders:order_detail", args=[3, "salkjdskljtlkwja03"]))
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()
        
        with pytest.raises(Http404):
            resp = order_detail(req, 4, "dklakdlaj-d4kj9")
        
    def test_uses_correct_template(self):
        order = mixer.blend(Order)
        resp = self.client.get(reverse_lazy(
            "orders:order_detail", args=[order.id, order.tx_ref]))
        self.assertTemplateUsed(resp, "orders/order/order_detail.html")
    
    def test_order_in_context(self):
        order = mixer.blend(Order)
        resp = self.client.get(reverse_lazy(
            "orders:order_detail", args=[order.id, order.tx_ref]))
        self.assertIn("order", resp.context)
    
    def test_order_in_context_not_empty(self):
        order = mixer.blend(Order)
        resp = self.client.get(reverse_lazy(
            "orders:order_detail", args=[order.id, order.tx_ref]))
        self.assertTrue(resp.context['order'])
