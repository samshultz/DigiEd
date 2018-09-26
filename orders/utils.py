import string
import random

def transaction_reference_generator(size=15, chars=string.digits + string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))


def create_order_items(cart, order, order_item):
    """
    docstring here
        :param cart: a dict of dict
        :param order: a queryset
    """
    for item in cart:
        order_item.objects.create(order=order,
                                 book=item['book'],
                                 price=item['price'],
                                 quantity=item['quantity'])
