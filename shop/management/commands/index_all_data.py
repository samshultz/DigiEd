from django.core.management import BaseCommand

import elasticsearch_dsl
import elasticsearch_dsl.connections
from shop.es_docs import ESBook
from shop.models import Book


class Command(BaseCommand):
    help = "Index all data to Elasticsearch"
    def handle(self, *args, **options):
        elasticsearch_dsl.connections.connections.create_connection()
        for book in Book.objects.all():
            
            esp = ESBook(meta={'id': book.pk},
                     title=book.name,
                     image=book.image.url,
                     url=book.get_absolute_url(),
                     price=book.price,
                     publisher=book.publisher,
                     author=book.author,
                     download_link=book.book_file.url

                     )
        
        
            esp.save(index='books')
        