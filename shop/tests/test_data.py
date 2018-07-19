import datetime

from django.core.exceptions import ValidationError

from django.utils import timezone

from ..models import Book, Category


def create_book_instance(title="Django By Example", price=2000, isbn="1234567890", category=None, year=datetime.date.today()):
    if not category:
        category = Category.objects.create(
            name="Web design",
            slug="web-design"
        )

    return Book.objects.create(
        category=category,
        title="Django By Example",
        author="Antonio Mele",
        image="/media/books/2018/07/19/517k0XB9ogL._SX302_BO1204203200_.jpg",
        book_file="ahk.pdf",
        price=price,
        isbn=isbn,
        year=year,

    )
