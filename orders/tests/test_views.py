import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from django.db import IntegrityError
from django.http import Http404
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy
from mock import patch

from cart.cart import Cart
from mixer.backend.django import mixer
from shop.tests.test_data import create_book_instance

from orders.models import Order, OrderItem
from ..views import confirm_payment, order_create, order_detail, order_list


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

    def test_view_for_non_authenticated_user(self):
        resp = self.client.get(reverse_lazy("orders:order_create"))
        self.assertTemplateUsed(resp, "orders/order/checkout_options.html")

    def test_auto_create_order_for_auth_user(self):

        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        c.login(username='jacob', password='top_secret')
        resp = c.get(reverse_lazy("orders:order_create"))

        self.assertEqual(Order.objects.count(), 1)
        self.assertTemplateUsed(resp, "orders/order/created.html")
        self.assertIn('order', resp.context)
        self.assertEqual(resp.context['order'].email, 'jacob@gmail.com')

    def test_auto_create_order_for_auth_user_with_first_name_last_name(self):

        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com',
            password='top_secret',
            first_name="Jacob", last_name="Kane")
        c.login(username='jacob', password='top_secret')
        resp = c.get(reverse_lazy("orders:order_create"))

        self.assertEqual(Order.objects.count(), 1)
        self.assertTemplateUsed(resp, "orders/order/created.html")
        self.assertIn('order', resp.context)
        self.assertEqual(resp.context['order'].first_name, 'Jacob')
        self.assertEqual(resp.context['order'].last_name, 'Kane')

    def test_auth_user_order_contains_order_items(self):
        req = RequestFactory().get(reverse_lazy("orders:order_create"))
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()
        # create a book instance and add it to cart
        book = create_book_instance()
        ct = Cart(req)
        ct.add(book)
        user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        req.user = user
        resp = order_create(req)
        order = Order.objects.first()
        self.assertGreaterEqual(order.items.count(),
                                1, "Order should contain atleast one item")


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
        req = RequestFactory().get(reverse_lazy(
            "orders:order_detail", args=[3, "salkjdskljtlkwja03"]))
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


class TestGuestCheckout(TestCase):
    def test_correct_template_was_used(self):
        resp = self.client.get(reverse_lazy("orders:order_form"))
        self.assertTemplateUsed(resp, "orders/order/create.html")

    def test_form_in_context(self):
        resp = self.client.get(reverse_lazy("orders:order_form"))
        self.assertIn('form', resp.context)


class TestOrderList(TestCase):
    def test_non_auth_users_redirected(self):
        resp = self.client.get(reverse_lazy("orders:order_list"))
        self.assertEqual(resp.status_code, 302)

    def test_orders_in_context(self):
        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
        order = mixer.blend(Order, email='jacob@gmail.com')
        c.login(username='jacob', password='top_secret')
        resp = c.get(reverse_lazy("orders:order_list"))

        self.assertTemplateUsed(resp, 'orders/order/order_list.html')
        self.assertIn('orders', resp.context)

    def test_return_last_page_when_empty_page_requested(self):
        for _ in range(23):
            mixer.blend(Order, email='jacob@gmail.com')

        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

        c.login(username='jacob', password='top_secret')
        resp = c.get(reverse_lazy("orders:order_list"), {'page': 3})
        self.assertEqual(len(resp.context['orders']), 3)

    def test_return_first_page_when_non_int_page_requested(self):
        for _ in range(23):
            mixer.blend(Order, email='jacob@gmail.com')

        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

        c.login(username='jacob', password='top_secret')
        resp = c.get(reverse_lazy("orders:order_list"), {'page': 'y'})
        self.assertEqual(len(resp.context['orders']), 20)
