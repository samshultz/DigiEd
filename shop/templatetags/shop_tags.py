from django import template
register = template.Library()

from ..models import Book, Category

@register.inclusion_tag('templatetagshtml/new_books.html')
def show_new_books(count=5):
    new_books = Book.objects.order_by('-year')[:count]
    return {'new_books': new_books}