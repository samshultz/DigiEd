from shop.es_docs import ESBook
from mixer.backend.django import mixer
from django.test import TestCase
from .test_data import create_book_instance
from elasticsearch_dsl.connections import connections

class TestESBook(TestCase):
    def setUp(self):
        connections.create_connection(hosts=['localhost'], timeout=20)

    def test_can_add_items_to_search_index(self):
        book = create_book_instance()
        ESBook.init(index="books")
        esp = ESBook(meta={'id': book.pk},
                     title=book.name,
                     image=book.image.url,
                     url=book.get_absolute_url(),
                     price=book.price,
                     publisher=book.publisher,
                     author=book.author,
                     download_link=book.book_file.url

                     )
        s = esp.save(index="books")
        self.assertTrue(s)
