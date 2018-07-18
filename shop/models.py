import datetime
import os

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from .validators import (validate_isbn_len, validate_price,
                         validate_year_is_not_future)

ALLOWED_EXTENSIONS = ['pdf']


class Category(models.Model):

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    class Meta:
        ordering = 'name',
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:product_list_by_category", kwargs={"category_slug": self.slug})
    


class Book(models.Model):
    category = models.ForeignKey(
        Category, related_name='books', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    author = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='books/%Y/%m/%d')
    book_file = models.FileField(
        upload_to='books/file/%Y/%m/%d', max_length=100,
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS,
                                           "Only pdf files are allowed")])
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, validators=[validate_price])

    year = models.DateField(default=timezone.now, validators=[
                            validate_year_is_not_future])
    num_pages = models.IntegerField("Number of pages", default=100)
    publisher = models.CharField(max_length=100)
    isbn = models.CharField(
        max_length=13, blank=True, null=True, validators=[validate_isbn_len])

    file_format = models.CharField(max_length=10, default="PDF")
    tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = 'title',
        index_together = (('id', 'slug'),)

    def clean(self):
        _, ext = os.path.splitext(self.book_file.name)
        if self.isbn:
            if len(self.isbn) < 10 or len(self.isbn) in (11, 12):
                raise ValidationError('ISBN must be 10 or 13 characters long')
        if self.price:
            if self.price < 0:
                raise ValidationError("Price can't be negative")
        if ext != ".pdf":
            raise ValidationError("Only PDF files are allowed")
        if self.year.year > datetime.date.today().year:
            raise ValidationError("Year cannot be in the future")

    def __str__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def save(self, *args, **kwargs):
        self.clean()
        if not self.slug:
            self.slug = slugify(self.title)
        super(Book, self).save(*args, **kwargs)  # Call the real save() method

    def get_absolute_url(self):

        return reverse('shop:book_detail', kwargs={'id': self.pk, 'slug': self.slug})
