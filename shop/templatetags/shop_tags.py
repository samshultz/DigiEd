from django import template
from cart.forms import CartAddProductForm
register = template.Library()

from ..models import Book, Category

@register.inclusion_tag('templatetagshtml/new_books.html')
def show_new_books(count=5):
    new_books = Book.objects.order_by('-year')[:count]
    return {'new_books': new_books}

@register.inclusion_tag('templatetagshtml/new_releases.html')
def show_new_releases(count=4):
    new_rel = Book.objects.order_by('-created')[:count]
    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    return {'new_releases': new_rel, 'cart_product_form': cart_product_form}