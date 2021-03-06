from celery import task
from django.core.mail import send_mail
from orders.models import Order
from django.urls import reverse_lazy


@task
def order_created(order_id, tx_ref):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    order = Order.objects.get(id=order_id, tx_ref=tx_ref)
    download_url = "http://dlearn.tk{}".format(reverse_lazy(
        "orders:order_detail", kwargs={'order_id': order_id, 'tx_ref': tx_ref}))
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
    Your order id is {}.\n\nClick on the link below to download \
    your resource. \n\n {}'.format(order.first_name, order.id, download_url)
    mail_sent = send_mail(subject, message, 'snpet.hub@gmail.com', [order.email])

    return mail_sent
