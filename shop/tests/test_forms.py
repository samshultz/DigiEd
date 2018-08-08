from django.test import TestCase
from shop.forms import SearchForm, UserEditForm
# from taggit.managers import TaggableManager



class TestSearchForm(TestCase):

    def test_form_without_data(self):
        form = SearchForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('q', form.errors)
        
    
    def test_form_with_valid_data(self):
        data = {"q": "DJango by Example"}
        form = SearchForm(data=data)
        self.assertTrue(form.is_valid())

