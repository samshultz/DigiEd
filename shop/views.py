from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Book, Category
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    books = Book.objects.all()
    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)

    return render(request,
                  'shop/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'books': books,
                   'cart_product_form': cart_product_form})


def product_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug)
    categories = Category.objects.all()
    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    book_tags_ids = book.tags.values_list('id', flat=True)
    similar_books = Book.objects.filter(tags__in=book_tags_ids)\
        .exclude(id=book.id)
    similar_books = similar_books.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-year')[:4]
    return render(request,
                  'shop/product_detail.html',
                  {'book': book, 'categories': categories,
                   'similar_books': similar_books,
                   'cart_product_form': cart_product_form})
