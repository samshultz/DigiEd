from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from cart.forms import CartAddProductForm
from elasticsearch_dsl import Search
from pages.models import DiscountSection
from shop.forms import SearchForm, UserEditForm
from newsletter.models import Newsletter
from .models import Book, Category


def home(request):
    featured = Book.objects.filter(featured=True).first()
    discount = DiscountSection.objects.filter(active=True).first()
    cart_product_form = CartAddProductForm(initial={'quantity': "1",
                                                    'update': False})
    total_books = Book.objects.count()
    # newsletter = Newsletter.objects.first()
    newsletter = "new-books"
    return render(request, "shop/home.html",
                  {'featured': featured,
                   'cart_product_form': cart_product_form,
                   'discount': discount,
                   'newsletter': newsletter,
                   'total_books': total_books})


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
            query = form.cleaned_data["q"]
            s = Search(index=["books"]).query(
                "multi_match",
                query=query,
                fields=['title', 'author', 'publisher'])
            results = s.execute()
            results = results.hits
            total_results = len(results)

            paginator = Paginator(results, 12)
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


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = UserEditForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'account/profile_edit.html', {'form': form})


@login_required
def profile_view(request):
    user = get_object_or_404(User, email=request.user.email)

    profile_upto_date = all([user.email, user.first_name,
                             user.last_name, user.username])
    return render(request, "account/profile_view.html",
                  {'user': user,
                   "profile_upto_date": profile_upto_date})
