import datetime

from django.core.exceptions import ValidationError

from django.utils import timezone

from ..models import Book, Category


def create_book_instance(title="Django By Example",
                         price=2000,
                         image="/books/2018/07/21/9781784391911.png",
                         isbn="1234567890",
                         category=None, year=datetime.date.today()):
    if not category:
        category = Category.objects.create(
            name="Web design",
            slug="web-design"
        )

    return Book.objects.create(
        category=category,
        title=title,
        author="Antonio Mele",
        image=image,
        book_file="ahk.pdf",
        price=price,
        isbn=isbn,
        year=year,

    )
