from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404, render

from cart.cart import Cart
from paystackapi.paystack import Paystack

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created
from .utils import create_order_items


def order_create(request):
    ctx = {}
    cart = Cart(request)
    payment_public_key = settings.PAYSTACK_PUBLIC_KEY
    ctx['payment_public_key'] = payment_public_key
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            create_order_items(cart, order, OrderItem)

            ctx['order'] = order
            ctx['cart'] = cart
            order_created.delay(order.id, order.tx_ref)

            return render(request, 'orders/order/created.html', ctx)
    else:

        if request.user.is_authenticated:
            first_name = request.user.first_name or request.user.username
            last_name = request.user.last_name or request.user.username

            email = request.user.email
            order = Order.objects.create(first_name=first_name,
                                         last_name=last_name,
                                         email=email)
            create_order_items(cart, order, OrderItem)
            ctx['order'] = order
            return render(request, 'orders/order/created.html', ctx)

        else:
            return render(request, 'orders/order/checkout_options.html')


def guest_checkout(request):
    # display an order form
    form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'form': form})


def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    cart = Cart(request)
    paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
    response = paystack.transaction.verify(reference=order.tx_ref)

    if response['data']['status'] == "success":
        if response['data']['amount'] == (cart.get_total_price() * 100):
            order.paid = True
            order.save()
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id, order.tx_ref)
            return render(request, 'orders/order/done.html',
                          {'order': order})
    else:
        status = response['data']['status']
        gateway_response = response['data']['gateway_response']
        return render(request, "orders/order/failed.html",
                      {'status': status, "response": gateway_response})


@login_required
def order_list(request):
    # get all orders by a customer
    object_list = Order.objects.filter(email=request.user.email)
    user = request.user
    profile_upto_date = all([user.email, user.first_name,
                             user.last_name, user.username])
    paginator = Paginator(object_list, 20)
    page = request.GET.get('page')
    try:

        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        orders = paginator.page(paginator.num_pages)
    return render(request, 'orders/order/order_list.html',
                  {'orders': orders,
                   'profile_update': profile_upto_date})


def order_detail(request, order_id, tx_ref):
    order = get_object_or_404(Order, id=order_id, tx_ref=tx_ref)
    profile_upto_date = None
    if request.user.is_authenticated:
        user = request.user
        profile_upto_date = all([user.email, user.first_name,
                             user.last_name, user.username])
    return render(request, "orders/order/order_detail.html", {'order': order, 'profile_update': profile_upto_date})
