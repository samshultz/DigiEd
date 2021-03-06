import datetime
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from mixer.backend.django import mixer
from taggit.managers import TaggableManager

from ..models import Book, Category
from .test_data import create_book_instance


class TestBookModel(TestCase):
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

    def test_raises_error_if_no_image_and_image_url_is_not_provided(self):
        with self.assertRaises(ValidationError):
            Book.objects.create(
            category=self.category,
            title="Application in Writing",
            author="Antonio Mele",
            book_file="ahk.pdf",
            price=2000,
            isbn="1234567890"

        )

    def test_raises_error_if_no_book_and_book_url_is_not_provided(self):
        with self.assertRaises(ValidationError):
            Book.objects.create(
            category=self.category,
            title="Application in Writing",
            author="Antonio Mele",
            image_url="http://ebook-dl.com/love-is-beautiful.jpg",
            price=2000,
            isbn="1234567890"

        )

    def test_book_was_created(self):
        self.assertEqual(Book.objects.count(), 1)

    def test_string_representation(self):
        self.assertEqual("Django By Example", str(self.book))

    def test_raise_validation_error_for_invalid_isbn(self):
        try:
            create_book_instance(isbn="123456789")

            self.fail("ISBN must be 10 or 13 characters long")
        except ValidationError:
            pass

    def test_reject_negative_prices(self):
        try:
            create_book_instance(price=-2000)

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

    def test_name_attr_returns_title(self):
        book = create_book_instance(title="New Book")
        self.assertEqual(book.title, book.name)

    def test_only_one_item_featured(self):
        category1 = mixer.blend("shop.Category")
        category2 = mixer.blend("shop.Category")
        create_book_instance(featured=True, category=category1)
        create_book_instance(featured=True, category=category2)
        featured_books = Book.objects.filter(featured=True)
        self.assertEqual(len(featured_books), 1)

    def test_book_saved_without_image_provided(self):
        category = mixer.blend("shop.Category")
        self.book = Book.objects.create(
            category=category,
            title="Django Example",
            author="Antonio Mele",
            image_url="http://ebook-dl.com/pictures/books/2-advanced-technologies-systems-mirsad-hadzikadic6992(www.ebook-dl.com)_Large.jpg",
            book_file="ahk.pdf",
            price=2000,
            isbn="1234567890"

        )
        self.assertEqual(Book.objects.count(), 2)

    def test_book_saved_without_book_file_provided(self):
        category = mixer.blend("shop.Category")
        self.book = Book.objects.create(
            category=category,
            title="Django Example",
            author="Antonio Mele",
            image="ahk.pdf",
            book_url="http://ebook-dl.com/dlbook/108393",
            price=2000,
            isbn="1234567890"

        )
        self.assertEqual(Book.objects.count(), 2)


class CategoryModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(
            name="Applications Development",
            slug="applications-development")

    def test_can_create_category(self):
        self.assertEqual(Category.objects.count(), 1)

    def test_slug_set_without_explicitly_setting_it(self):
        category = Category.objects.create(
            name="lovering how"
        )
        self.assertEqual(category.slug, "lovering-how")

    def test_string_representation(self):
        self.assertEqual("Applications Development", str(self.cat))

    def test_get_absolute_url(self):
        self.assertEqual("/shop/applications-development/",
                         self.cat.get_absolute_url())

    def test_category_slug_is_unique(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name="Applications Development",
                slug="applications-development")
