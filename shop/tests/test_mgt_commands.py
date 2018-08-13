from django.test import TestCase
from django.core.management import call_command


class TestIndexDataCommand(TestCase):

    def test_command(self):
        args = []
        opts = {}

        com = call_command('index_all_data', *args, **opts)
        self.assertIsNone(com)
        
    