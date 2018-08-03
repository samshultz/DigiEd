import datetime

from django.core.exceptions import ValidationError

from django.utils import timezone

from ..models import Book, Category
from django.core.files.uploadedfile import SimpleUploadedFile


def create_book_instance(title="Django By Example",
                         price=2000,
                         image=SimpleUploadedFile(name='test_image.jpg', content=open(
                             r"C:\Users\Samshultz\Pictures\never-regret.jpg", 'rb').read(), content_type='image/jpeg'),
                         isbn="1234567890",
                         category=None, year=datetime.date.today(),
                         featured=False,
                         discount_price=0):
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
        featured=featured,
        discount_price=discount_price
    )
