from django.test import RequestFactory, TestCase

from .test_data import create_book_instance
# from .test_data import test_data
from ..views import product_detail, product_list


class ProductViewTest(TestCase):
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
