import pytest
from django.core.exceptions import ObjectDoesNotExist

from mixer.backend.django import mixer
from django.test import TestCase
from ..models import Order
from ..tasks import order_created


class TestOrderCreated(TestCase):
    def test_send_mail_when_called_with_correct_arguments(self):
        order = mixer.blend(Order)
        sent = order_created(order.id, order.tx_ref)
        self.assertEqual(sent, 1)

    def test_raises_error_when_called_with_wrong_arguments(self):
        with pytest.raises(ObjectDoesNotExist):
            order_created(1, "loveisKinKd")
