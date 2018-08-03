
import os
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError


def validate_isbn_len(value):
    """ Validates that the ISBN provided is either 10 or 13 characters long"""
    if value:
        if len(value) < 10 or len(value) in (11, 12) or len(value) > 13:
            raise ValidationError('ISBN must be 10 or 13 characters long')

def validate_price(value):
    """ Validates that the price is not negative"""
    if value:
        if value < 0:
            raise ValidationError("Price can't be negative")

def validate_year_is_not_future(value):
    if value.year > datetime.date.today().year:
        raise ValidationError("Year cannot be in the future")
