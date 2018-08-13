from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Book
from .cart import Cart
from .forms import CartAddProductForm


@require_POST
def cart_add(request, book_id):

    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
    
        cart.add(book=book)
    return redirect('cart:cart_detail')

def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    cart.remove(book)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    profile_upto_date = None
    if request.user.is_authenticated:
        user = request.user
        profile_upto_date = all([user.email, user.first_name,
                             user.last_name, user.username])
    return render(request, 'cart/detail.html', {'cart': cart, 'profile_update': profile_upto_date})