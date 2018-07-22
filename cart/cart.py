from decimal import Decimal
from django.conf import settings
from shop.models import Book


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book, quantity=1):
        """
        Add a product to the cart or update its quantity.
        """
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {
                'quantity': 1, 'price': str(book.price)}
        # if update_quantity:
        #     self.cart[book_id]['quantity'] = quantity
        # else:
        #     self.cart[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, book):
        """
        Remove a product from the cart.
        """
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        book_ids = self.cart.keys()
        # get the product objects and add them to the cart
        books = Book.objects.filter(id__in=book_ids)

        for book in books:
            self.cart[str(book.id)]['book'] = book

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
