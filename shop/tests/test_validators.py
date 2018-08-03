import datetime

import pytest
from django.core.exceptions import ValidationError

from django.test import TestCase
from django.utils import timezone

from shop.validators import validate_isbn_len, validate_price, validate_year_is_not_future
pytestmark = pytest.mark.django_db

class TestValidators(TestCase):

    def test_validate_isbn_with_less_than_10_chars(self):
        
        with self.assertRaises(ValidationError):
            validate_isbn_len("123456789")

    def test_validate_isbn_with_more_than_13_chars(self):
        
        with self.assertRaises(ValidationError):
            validate_isbn_len("12345678901234")
    
    def test_validate_isbn_with_more_than_10_and_less_than_13_chars(self):
        
        with self.assertRaises(ValidationError):
            validate_isbn_len("12345678903")

    def test_validate_price_with_negative_value(self):
        with self.assertRaisesMessage(ValidationError, "Price can't be negative"):
            validate_price(-100)

    def test_validate_year_not_future_with_future_date(self):
        future_date = timezone.now() + datetime.timedelta(days=369)
        with self.assertRaisesMessage(ValidationError, "Year cannot be in the future"):
            validate_year_is_not_future(future_date)
            