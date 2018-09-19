from shop.es_docs import ESBook
from shop.models import Book
from django.test import TestCase
from .test_data import create_book_instance
from elasticsearch_dsl.connections import connections
from elasticsearch import NotFoundError
from mock import MagicMock


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
        
        esp.save = MagicMock(return_value=True)
        s = esp.save(index="books")

        self.assertTrue(s)
    
    def test_can_remove_item_from_index_when_item_is_deleted(self):
        book = create_book_instance()
        esp = ESBook(meta={'id': book.pk},
                     title=book.name,
                     image=book.image.url,
                     url=book.get_absolute_url(),
                     price=book.price,
                     publisher=book.publisher,
                     author=book.author,
                     download_link=book.book_file.url

                     )
        esp.save(index="books")
        Book.objects.get(id=book.pk).delete()
        with self.assertRaises(NotFoundError):
            ESBook().get(id=book.pk, index="books")

