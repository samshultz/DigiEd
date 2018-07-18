import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ..models import Book, Category
from .test_data import create_book_instance


class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Web development",
            slug="web-development"
        )

        self.book = Book.objects.create(
            category=self.category,
            title="Django By Example",
            author="Antonio Mele",
            image="ahs.jpg",
            book_file="ahk.pdf",
            price=2000,
            isbn="1234567890"

        )

    def test_book_was_created(self):
        self.assertEqual(Book.objects.count(), 1)

    def test_string_representation(self):
        self.assertEqual("Django By Example", str(self.book))

    def test_raise_validation_error_for_invalid_isbn(self):
        try:
            book = create_book_instance(isbn="123456789")

            self.fail("ISBN must be 10 or 13 characters long")
        except ValidationError:
            pass

    def test_reject_negative_prices(self):
        try:
            book = create_book_instance(price=-2000)

            self.fail("Price can't be negative")
        except ValidationError:
            pass

    def test_published_year_with_future_date(self):

        time = timezone.now() + datetime.timedelta(days=365)

        try:
            create_book_instance(year=time)
            self.fail("Year must not be in the future")
        except ValidationError:
            pass

    def test_slug(self):
        self.assertEqual("django-by-example", self.book.slug)

    def test_get_absolute_url(self):
        book = create_book_instance(year=datetime.date.today())
        self.assertEqual(
            "/shop/{}/django-by-example/".format(book.id), book.get_absolute_url())


class CategoryModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            name="Applications Development",
            slug="applications-development")

    def test_can_create_category(self):
        self.assertEqual(Category.objects.count(), 1)

    def test_string_representation(self):
        self.assertEqual("Applications Development", str(self.cat))

    def test_get_absolute_url(self):
        self.assertEqual("/shop/applications-development/", self.cat.get_absolute_url())
