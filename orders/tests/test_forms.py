from django.test import TestCase
from ..forms import OrderCreateForm
# from taggit.managers import TaggableManager

from shop.tests.test_data import create_book_instance


class TestOrderCreateForm(TestCase):

    def test_form_without_data(self):
        form = OrderCreateForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)
    
    def test_form_with_valid_data(self):
        data = {"first_name": "Sam", 'last_name': "James", "email": "admin@mail.com"}
        form = OrderCreateForm(data=data)
        self.assertTrue(form.is_valid())