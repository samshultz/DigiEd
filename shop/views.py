from django.shortcuts import render, get_object_or_404

from .models import Book, Category


def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    books = Book.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)

    return render(request,
                  'shop/product_list.html',
                  {'category': category,
                   'categories': categories,
                   'books': books})


def product_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug)
    return render(request,
                  'shop/product_detail.html',
                  {'book': book})
