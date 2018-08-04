import pytest
from django.test import RequestFactory, TestCase
from django.core.paginator import EmptyPage
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse_lazy
# from .test_data import test_data
from ..views import product_detail, product_list, home, search
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
        book1 = create_book_instance(category=category1)
        book2 = create_book_instance(category=category2)
        book3 = create_book_instance(category=category1)
        book4 = create_book_instance(category=category2)
        book5 = create_book_instance(category=category1)
        book6 = create_book_instance(category=category1)
        book7 = create_book_instance(category=category2)
        book8 = create_book_instance(category=category1)
        book9 = create_book_instance(category=category2)
        book10 = create_book_instance(category=category1)
        
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
        resp = self.client.get(reverse_lazy("search"), data={"q": "Django", "page": 10})
        self.assertTrue(resp.context['results'])