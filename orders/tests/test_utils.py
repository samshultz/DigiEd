from django.test import TestCase

from ..utils import transaction_reference_generator


class TestTransactionReferenceGenerator(TestCase):
    def test_len_equal_size(self):
        tx_ref = transaction_reference_generator()
        self.assertEqual(len(tx_ref), 15, "tx_ref length should equal size")
        tx_ref = transaction_reference_generator(size=30)
        self.assertEqual(len(tx_ref), 30)

    def test_return_value_equal_string(self):
        tx_ref = transaction_reference_generator()
        self.assertEqual(type(tx_ref), str, "should return a string value")
