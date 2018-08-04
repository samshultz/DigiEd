from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections
from pages.models import DiscountSection
from shop.forms import SearchForm

from .models import Book, Category


def home(request):
    featured = Book.objects.filter(featured=True).first()
    discount = DiscountSection.objects.filter(active=True).first()
    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    return render(request, "shop/home.html",
                  {'featured': featured,
                   'cart_product_form': cart_product_form,
                   'discount': discount})


def product_list(request, category_slug=None):

    category = None
    categories = Category.objects.all()
    object_list = Book.objects.only('image', 'price', 'book_file').all()
    discount = DiscountSection.objects.filter(active=True).first()

    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category=category).only(
            'image', 'price', 'book_file')

    paginator = Paginator(object_list, 9)
    page = request.GET.get('page')
    try:

        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        books = paginator.page(paginator.num_pages)

    return render(request,
                  'shop/product_list.html',
                  {'category': category,
                   'page_obj': page,
                   'categories': categories,
                   'books': books,
                   'cart_product_form': cart_product_form,
                   'discount': discount})


def product_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug)
    categories = Category.objects.only('slug', 'name').all()
    discount = DiscountSection.objects.filter(active=True).first()
    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    book_tags_ids = book.tags.values_list('id', flat=True)
    similar_books = Book.objects.filter(tags__in=book_tags_ids)\
        .exclude(id=book.id).only('image', 'price', 'book_file')
    similar_books = similar_books.annotate(same_tags=Count('tags'))\
        .order_by('-same_tags', '-year')[:4]
    return render(request,
                  'shop/product_detail.html',
                  {'book': book, 'categories': categories,
                   'similar_books': similar_books,
                   'cart_product_form': cart_product_form,
                   'discount': discount})


def search(request):
    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            connections.create_connection()
            query = form.cleaned_data["q"]
            s = Search(index=["books"]).query(
                "multi_match",
                query=query,
                fields=['title', 'author', 'publisher'])
            results = s.execute()
            results = results.hits
            total_results = len(results)

            paginator = Paginator(results, 6)
            page = request.GET.get('page')
            try:

                results = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer deliver the first page
                results = paginator.page(1)
            except EmptyPage:
                # If page is out of range deliver last page of results
                results = paginator.page(paginator.num_pages)
            return render(request, "shop/search.html", {'results': results,
                                                        'total_results': total_results,
                                                        'query': query,
                                                        "cart_product_form": cart_product_form})
# http://127.0.0.1:8000/search/?q=O%27Reilly+Media%2C+Inc.&page=2
