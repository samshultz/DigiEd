import pytest
from django.test import RequestFactory, TestCase
from django.core.paginator import EmptyPage
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# from .test_data import test_data
from ..views import home
from django.http import Http404
from .test_data import create_book_instance
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db


class TestProductView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.book = create_book_instance()

    def test_correct_template_was_used_for_the_list_page(self):
        response = self.client.get("/shop/")
        self.assertEqual("shop/product_list.html", response.templates[0].name)

    def test_categories_in_context(self):
        response = self.client.get("/shop/")
        self.assertIn('categories', response.context)

    def test_category_in_context(self):
        response = self.client.get("/shop/")
        self.assertIn('category', response.context)

    def test_books_in_context(self):
        response = self.client.get("/shop/")
        self.assertIn('books', response.context)

    def test_book_in_detail_context(self):
        response = self.client.get(
            "/shop/{}/{}/".format(self.book.id, self.book.slug))
        self.assertIn('book', response.context)

    def test_correct_template_was_used_for_the_detail_page(self):
        response = self.client.get(
            "/shop/{}/{}/".format(self.book.id, self.book.slug))
        self.assertEqual("shop/product_detail.html",
                         response.templates[0].name)

    def test_list_view_returns_correct_queryset_when_called_with_category_slug(self):
        category1 = mixer.blend("shop.Category")
        category2 = mixer.blend("shop.Category")
        create_book_instance(category=category1)
        create_book_instance(category=category2)
        create_book_instance(category=category1)
        create_book_instance(category=category2)
        create_book_instance(category=category1)
        create_book_instance(category=category1)
        create_book_instance(category=category2)
        create_book_instance(category=category1)
        create_book_instance(category=category2)
        create_book_instance(category=category1)

        # when called with category slug
        resp = self.client.get("/shop/{}/".format(category1.slug))
        # should contain only books from that category
        self.assertEqual(len(resp.context['books']), 6)
        # when called with a page number
        pag = self.client.get("/shop/", {'page': 1})
        # should contain total of <=9 items
        self.assertEqual(len(pag.context['books']), 9)
        empty_pag = self.client.get("/shop/", {'page': 3})
        self.assertRaises(EmptyPage)
        self.assertEqual(len(empty_pag.context['books']), 2)

    def test_home_view(self):
        req = self.factory.get("/")
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()
        resp = home(req)

        self.assertEqual(resp.status_code, 200)

    def test_search_view_existing_data(self):
        resp = self.client.get(reverse_lazy("search"), data={"q": "Django"})

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "shop/search.html")
        self.assertIn('results', resp.context)

    def test_search_view_with_get_data(self):
        resp = self.client.get(reverse_lazy("search"), data={
                               "q": "Django", "page": 10})
        self.assertTrue(resp.context['results'])


class TestProfileEdit(TestCase):
    def test_redirect_for_anonymous_user(self):
        resp = self.client.get(reverse_lazy('profile_edit'))
        self.assertEqual(resp.status_code, 302)
    
    def test_view_with_get_request(self):
        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

        c.login(username='jacob', password='top_secret')

        resp = c.get(reverse_lazy('profile_edit'))
        self.assertEqual(resp.status_code, 200)


    def test_user_detail_were_updated_with_valid_data(self):
        data = {'first_name': "kenneth", "last_name": "Lord",
                'email': "jacob@gmail.com", "username": "jacob"}
        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

        c.login(username='jacob', password='top_secret')

        resp = c.post(reverse_lazy('profile_edit'), data=data)
        user = User.objects.first()
        self.assertEqual(user.first_name, "kenneth")
        msgs = [msg for msg in resp.context['messages']]
        self.assertEqual(str(msgs[0]), 'Profile updated successfully')
        self.assertEqual(msgs[0].tags, 'success')
    
    def test_threw_an_error_with_invalid_data(self):
        data = {'first_name': "kenneth", "last_name": "Lord"}
        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

        c.login(username='jacob', password='top_secret')

        resp = c.post(reverse_lazy('profile_edit'), data=data)
        user = User.objects.first()
        self.assertFalse(user.first_name)
        msgs = [msg for msg in resp.context['messages']]
        self.assertEqual(str(msgs[0]), 'Error updating your profile')
        self.assertEqual(msgs[0].tags, 'error')

class TestProfileView(TestCase):
    def test_redirect_for_anonymous_user(self):
        resp = self.client.get(reverse_lazy('profile_view'))
        self.assertEqual(resp.status_code, 302)
    
    def test_that_correct_template_was_used(self):
        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

        c.login(username='jacob', password='top_secret')

        resp = c.get(reverse_lazy('profile_view'))
        self.assertTemplateUsed(resp, "account/profile_view.html")

    
    def test_that_contains_correct_keys(self):
        c = self.client

        User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')

        c.login(username='jacob', password='top_secret')

        resp = c.get(reverse_lazy('profile_view'))
        self.assertIn('user', resp.context)
        self.assertIn('profile_upto_date', resp.context)
        self.assertEqual(type(resp.context['profile_upto_date']), bool)
        self.assertEqual(type(resp.context['user']), User)