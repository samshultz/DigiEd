import datetime

from django.core.exceptions import ValidationError

from django.utils import timezone

from ..models import Book, Category


def create_book_instance(price=2000, isbn="1234567890", year=datetime.date.today()):
    category = Category.objects.create(
        name="Web design",
        slug="web-design"
    )
    return Book.objects.create(
        category=category,
        title="Django By Example",
        author="Antonio Mele",
        image="ahs.jpg",
        book_file="ahk.pdf",
        price=price,
        isbn=isbn,
        year=year,

    )
