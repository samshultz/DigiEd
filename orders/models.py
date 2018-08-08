from django.db import models
from shop.models import Book
from .utils import transaction_reference_generator
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    # Transaction Reference
    tx_ref = models.CharField(
        max_length=30, blank=True, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.tx_ref:
            self.tx_ref = transaction_reference_generator()
        super(Order, self).save(*args, **kwargs)  # Call the real save() method


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items')
    book = models.ForeignKey(Book,
                             related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[
                                MinValueValidator(0, "Prices can't be negative")])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    def clean(self):
        if self.price < 0:
            raise ValidationError("Prices can't be negative")
        if self.quantity < 0:
            raise ValidationError("Quantity can't be negative")

    def save(self, *args, **kwargs):
        self.clean()
        # Call the real save() method
        super(OrderItem, self).save(*args, **kwargs)
