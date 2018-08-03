from django.conf import settings
from django.shortcuts import get_object_or_404, render

from cart.cart import Cart
from paystackapi.paystack import Paystack

from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         book=item['book'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # # clear the cart
            # cart.clear()
            return render(request,
                          'orders/order/created.html',
                          {'order': order,
                           'cart': cart})
    else:
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})


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


def order_list(request):
    # get all orders by a customer
    # pass it to the context
    # template_name = 'orders/order/order_list.html
    pass


def order_detail(request, order_id, tx_ref):
    order = get_object_or_404(Order, id=order_id, tx_ref=tx_ref)
    
    return render(request, "orders/order/order_detail.html", {'order': order})
    
